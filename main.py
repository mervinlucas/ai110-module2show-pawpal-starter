"""Command-line demo for PawPal+: builds an owner with pets and tasks, then prints today's plan."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Set up sample data and print today's schedule."""
    owner = Owner("Jordan", available_minutes=60)

    biscuit = Pet("Biscuit", "dog")
    mochi = Pet("Mochi", "cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    biscuit.add_task(Task("Morning walk", 30, "high"))
    biscuit.add_task(Task("Brushing", 15, "low"))
    mochi.add_task(Task("Feeding", 10, "high"))
    mochi.add_task(Task("Give medicine", 5, "high"))
    mochi.add_task(Task("Play time", 20, "medium"))

    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    print(f"Today's Schedule for {owner.name} ({owner.available_minutes} min available)")
    print("=" * 50)
    for number, task in enumerate(plan, start=1):
        print(f"{number}. {task.title} - {task.duration_minutes} min [priority: {task.priority}]")

    print()
    print("Why this plan:")
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
