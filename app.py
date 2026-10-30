"""Streamlit UI for PawPal+: add pets, give them care tasks, and build today's plan."""

from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Add your pets and their care tasks, then build a plan that fits your day.")

# Streamlit reruns this whole file on every click, so the Owner is kept in
# session_state. Otherwise every pet and task would be lost after each interaction.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", available_minutes=60)

owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)

# --- Owner info ---
st.subheader("👤 Owner")
col1, col2 = st.columns(2)
with col1:
    owner.name = st.text_input("Owner name", value="Jordan", key="owner_name")
with col2:
    owner.available_minutes = int(
        st.number_input(
            "Time available today (minutes)",
            min_value=0,
            max_value=1440,
            value=60,
            key="available_minutes",
        )
    )

st.divider()

# --- Add a pet ---
st.subheader("🐶 Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        pet_name = pet_name.strip()
        if not pet_name:
            st.warning("Please enter a pet name.")
        elif any(p.name == pet_name for p in owner.pets):
            # Names must be unique because the task form picks pets by name.
            st.warning(f"You already have a pet named {pet_name}.")
        else:
            owner.add_pet(Pet(pet_name, species))
            st.success(f"Added {pet_name}!")

st.divider()

# --- Add a task to a pet ---
st.subheader("📝 Add a Task")
if not owner.pets:
    st.info("Add a pet first, then you can give it tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        # Pick the pet by name, then look up the real Pet object stored on the owner.
        pet_name_choice = st.selectbox("Pet", [p.name for p in owner.pets])
        pet = next(p for p in owner.pets if p.name == pet_name_choice)

        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title")
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        col4, col5 = st.columns(2)
        with col4:
            start_time = st.time_input("Start time", value=time(8, 0), step=300)
        with col5:
            frequency = st.selectbox("Repeats", ["once", "daily", "weekly"])

        if st.form_submit_button("Add task"):
            if task_title.strip():
                pet.add_task(
                    Task(
                        task_title.strip(),
                        int(duration),
                        priority,
                        time=start_time.strftime("%H:%M"),
                        frequency=frequency,
                    )
                )
                st.success(f"Added '{task_title.strip()}' for {pet.name}.")
            else:
                st.warning("Please enter a task title.")

st.divider()

# --- Show pets and their tasks ---
st.subheader("📋 Your Pets and Tasks")
if not owner.pets:
    st.info("No pets yet.")
else:
    col1, col2 = st.columns(2)
    with col1:
        pet_filter = st.selectbox("Show pet", ["All pets"] + [p.name for p in owner.pets])
    with col2:
        status_filter = st.selectbox("Show status", ["All", "To do", "Done"])

    # Turn the status choice into the value filter_tasks expects (None means "any").
    completed_filter = {"All": None, "To do": False, "Done": True}[status_filter]

    for pet in owner.pets:
        if pet_filter != "All pets" and pet.name != pet_filter:
            continue
        st.markdown(f"**{pet.name}** ({pet.species})")
        tasks = scheduler.sort_by_time(scheduler.filter_tasks(pet.name, completed_filter))
        if tasks:
            st.table(
                [
                    {
                        "Time": task.time or "--:--",
                        "Task": task.title,
                        "Duration (min)": task.duration_minutes,
                        "Priority": task.priority,
                        "Repeats": task.frequency,
                        "Due": str(task.due_date),
                        "Done": "✅" if task.completed else "",
                    }
                    for task in tasks
                ]
            )
        else:
            st.caption("No matching tasks.")

st.divider()

# --- Mark a task complete ---
st.subheader("✅ Complete a Task")
# Show the message saved by the last "Mark complete" click (it survives the rerun below).
if "done_message" in st.session_state:
    st.success(st.session_state.pop("done_message"))

pets_with_todo = [p for p in owner.pets if scheduler.filter_tasks(p.name, completed=False)]
if not pets_with_todo:
    st.info("No unfinished tasks.")
else:
    done_pet_name = st.selectbox("Pet", [p.name for p in pets_with_todo], key="done_pet")
    done_pet = next(p for p in pets_with_todo if p.name == done_pet_name)
    todo_tasks = scheduler.sort_by_time(scheduler.filter_tasks(done_pet.name, completed=False))
    labels = [f"{t.time or '--:--'}  {t.title} (due {t.due_date})" for t in todo_tasks]
    task_choice = st.selectbox("Task", labels)

    if st.button("Mark complete"):
        task = todo_tasks[labels.index(task_choice)]
        next_task = done_pet.complete_task(task)
        if next_task is not None:
            st.session_state.done_message = (
                f"Done! '{task.title}' repeats {task.frequency}, so the next one is due {next_task.due_date}."
            )
        else:
            st.session_state.done_message = f"Done! '{task.title}' is complete."
        # Rerun so the task tables above show the change right away.
        st.rerun()

st.divider()

# --- Build today's schedule ---
st.subheader("📅 Today's Schedule")
if st.button("Generate schedule"):
    plan = scheduler.generate_plan()

    if plan:
        st.table(
            [
                {
                    "Time": task.time or "--:--",
                    "Task": task.title,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority,
                }
                for task in plan
            ]
        )
    else:
        st.info("Nothing fits in today's plan yet. Add tasks or increase your available time.")

    for warning in scheduler.detect_conflicts():
        st.warning(f"⚠️ Time conflict: {warning}")

    st.markdown("**Why this plan:**")
    st.text(scheduler.explain_plan())
