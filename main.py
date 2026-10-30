"""Command-line demo for PawPal+: builds an owner with pets and tasks, then prints today's plan."""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_plan(owner: Owner, scheduler: Scheduler) -> None:
    """Generate and print today's schedule, its explanation, and any time conflicts."""
    plan = scheduler.generate_plan()

    print(f"Today's Schedule for {owner.name} ({owner.available_minutes} min available)")
    print("=" * 50)
    for task in plan:
        print(f"{task.time or '--:--'}  {task.title} - {task.duration_minutes} min [priority: {task.priority}]")

    print()
    print("Why this plan:")
    print(scheduler.explain_plan())

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print()
        print("⚠️  Conflicts:")
        for warning in conflicts:
            print(f"  - {warning}")


def main() -> None:
    """Set up sample data and show sorting, filtering, recurring tasks, and conflicts."""
    owner = Owner("Jordan", available_minutes=60)

    biscuit = Pet("Biscuit", "dog")
    mochi = Pet("Mochi", "cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # Tasks are added out of order on purpose so sorting by time is visible.
    biscuit.add_task(Task("Morning walk", 30, "high", time="08:00", frequency="daily"))
    biscuit.add_task(Task("Brushing", 15, "low", time="18:00", frequency="weekly"))
    mochi.add_task(Task("Play time", 20, "medium", time="17:00"))
    mochi.add_task(Task("Feeding", 10, "high", time="07:30", frequency="daily"))
    mochi.add_task(Task("Give medicine", 5, "high", time="08:15"))  # overlaps the walk

    scheduler = Scheduler(owner)
    print_plan(owner, scheduler)

    print()
    print("Mochi's tasks (sorted by time):")
    for task in scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Mochi")):
        print(f"  {task.time}  {task.title}")

    # Completing a daily task automatically adds tomorrow's copy.
    print()
    walk = biscuit.tasks[0]
    next_walk = biscuit.complete_task(walk)
    print(f"Completed '{walk.title}'. Next one is due {next_walk.due_date}.")

    print()
    print("Completed tasks:")
    for task in scheduler.filter_tasks(completed=True):
        print(f"  {task.title}")


if __name__ == "__main__":
    main()
