# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run the CLI demo with:

```bash
python main.py
```

Sample output (one owner with 60 minutes, two pets, five tasks):

```
Today's Schedule for Jordan (60 min available)
==================================================
07:30  Feeding - 10 min [priority: high]
08:00  Morning walk - 30 min [priority: high]
08:15  Give medicine - 5 min [priority: high]
18:00  Brushing - 15 min [priority: low]

Why this plan:
Added 'Feeding' at 07:30 (high priority, 10 min).
Added 'Morning walk' at 08:00 (high priority, 30 min).
Added 'Give medicine' at 08:15 (high priority, 5 min).
Added 'Brushing' at 18:00 (low priority, 15 min).
Skipped 'Play time' (20 min): not enough time left.
Total time used: 60 of 60 min.

⚠️  Conflicts:
  - 'Morning walk' at 08:00 overlaps with 'Give medicine' at 08:15.

Mochi's tasks (sorted by time):
  07:30  Feeding
  08:15  Give medicine
  17:00  Play time

Completed 'Morning walk'. Next one is due 2026-10-31.

Completed tasks:
  Morning walk
```

## 🧪 Testing PawPal+

The tests live in `tests/test_pawpal.py` and use **pytest**. Run them from the project folder (with your virtual environment active):

```bash
# Run the full test suite:
pytest

# See each test's name and result:
pytest -v

# Optional: run with coverage (first install the plugin with `pip install pytest-cov`):
pytest --cov
```

`pytest.ini` tells pytest where the tests are and lets them import `pawpal_system`, so no extra setup is needed.

**What the tests cover (11 tests):**

| Area | What is checked |
|------|-----------------|
| Basics | `mark_complete()` sets `completed` to `True`; `add_task()` adds the task to the pet |
| Sorting by time | Tasks come back earliest first; tasks with no set time go last |
| Recurring tasks | Completing a daily task adds an unfinished copy due 1 day later; weekly adds one due 7 days later; a one-time task adds nothing; tomorrow's copy is not put in today's plan |
| Conflict detection | Overlapping tasks (08:00 for 30 min and 08:15) are flagged; back-to-back tasks (08:00 for 30 min, then 08:30) are **not**; tasks with no set time are never flagged |

Sample test output (`pytest -v`):

```
============================= test session starts ==============================
rootdir: <project folder>
configfile: pytest.ini
testpaths: tests
collecting ... collected 11 items

tests/test_pawpal.py::test_mark_complete_sets_completed_to_true PASSED   [  9%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 18%]
tests/test_pawpal.py::test_sort_by_time_orders_tasks_earliest_first PASSED [ 27%]
tests/test_pawpal.py::test_sort_by_time_puts_tasks_without_time_last PASSED [ 36%]
tests/test_pawpal.py::test_completing_daily_task_adds_copy_for_next_day PASSED [ 45%]
tests/test_pawpal.py::test_completing_weekly_task_adds_copy_for_next_week PASSED [ 54%]
tests/test_pawpal.py::test_completing_one_time_task_does_not_repeat PASSED [ 63%]
tests/test_pawpal.py::test_next_daily_task_is_not_in_todays_plan PASSED  [ 72%]
tests/test_pawpal.py::test_overlapping_tasks_are_flagged_as_conflict PASSED [ 81%]
tests/test_pawpal.py::test_back_to_back_tasks_do_not_conflict PASSED     [ 90%]
tests/test_pawpal.py::test_tasks_without_time_are_never_in_conflict PASSED [100%]

============================== 11 passed in 0.01s ==============================
```

## 📐 Smarter Scheduling

PawPal+ goes beyond a simple to-do list. All of this logic lives in `pawpal_system.py` and is used by both `main.py` and the Streamlit app.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_tasks()`, `Scheduler.sort_by_time()` | Tasks are **chosen** by priority (high first, then shortest), then the final plan is **shown** in time order. Tasks with no set time go last. |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Show tasks for one pet, only unfinished tasks, only finished tasks, or any mix. `None` means "any". `generate_plan()` also skips tasks that are done or not due until a later day. Tasks are skipped if time runs out. |
| Conflict handling | `Scheduler.detect_conflicts()`, `Task.start_minutes()`, `Task.end_minutes()` | Compares every pair of timed tasks and returns a warning when two overlap (e.g. a 30-min walk at 08:00 and meds at 08:15). Back-to-back tasks (08:00–08:30 then 08:30) are **not** a conflict. Conflicts are warnings only, so the plan is still shown. |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | A task can repeat `"once"`, `"daily"`, or `"weekly"`. Completing a daily/weekly task automatically adds a fresh copy due 1 or 7 days later. |

**New `Task` fields:** `time` (`"HH:MM"`, optional), `frequency` (`"once"` / `"daily"` / `"weekly"`), and `due_date` (defaults to today).

**In the Streamlit app:** the task form now has a start time and a "Repeats" option; the task list can be filtered by pet and status and sorted by time or priority (with a "Showing X of Y tasks" count); a "Complete a Task" section marks tasks done (and schedules the next one for repeating tasks); and the generated schedule shows a red banner listing any time conflicts at the top (or a green "No time conflicts" message).

## 📸 Demo Walkthrough

### Main features

- **Owner and pets:** enter your name and how many minutes you have today, then add as many pets as you like.
- **Care tasks:** give each pet tasks with a duration, priority, start time, and whether they repeat (once, daily, or weekly).
- **Sorting and filtering:** view tasks by pet and by status (to do / done), sorted by time or by priority.
- **Recurring tasks:** marking a daily or weekly task complete automatically creates the next one.
- **Daily plan:** PawPal+ picks the most important tasks that fit in your time, lists them in time order, and explains each choice.
- **Conflict warnings:** if two planned tasks overlap, you get a clear warning at the top of the schedule.

### How to run it

```bash
# 1. Set up once (see "Getting started" above)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Start the web app (opens in your browser, usually at http://localhost:8501)
streamlit run app.py

# Or run the command-line demo instead
python main.py
```

### Step by step

1. **Set up the owner.** At the top of the page, type your name and how many minutes you have for pet care today (for example, `60`).
2. **Add your pets.** In **🐶 Add a Pet**, enter a name (for example, *Biscuit*), pick a species, and click **Add pet**. Repeat for each pet (for example, *Mochi* the cat). Each pet needs a different name.
3. **Add care tasks.** In **📝 Add a Task**, pick a pet and enter a title, duration, priority, start time, and whether it repeats. For example:
   - Biscuit: *Morning walk*, 30 min, high, 08:00, daily
   - Mochi: *Give medicine*, 5 min, high, 08:15, once
   - Mochi: *Play time*, 20 min, medium, 17:00, once
4. **Review your tasks.** In **📋 Your Pets and Tasks**, use **Show pet** and **Show status** to narrow the list, and **Sort by** to switch between time order and priority order. The count at the bottom shows how many tasks match.
5. **Generate today's schedule.** In **📅 Today's Schedule**, click **Generate schedule**. With the example tasks above, a red banner warns that *Morning walk* (08:00–08:30) overlaps with *Give medicine* (08:15). Below it you'll see the plan in time order and a "Why this plan" explanation showing what was added, what was skipped, and how much time was used.
6. **Complete a task.** In **✅ Complete a Task**, pick Biscuit and *Morning walk*, then click **Mark complete**. Because it's a daily task, PawPal+ tells you the next one is due tomorrow, and it appears under **Show status → To do** with tomorrow's date.
7. **Generate again.** Click **Generate schedule** again. The finished walk (and tomorrow's copy) are no longer in today's plan, so the conflict is gone and you'll see a green **No time conflicts** message.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
