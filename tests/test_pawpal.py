"""Tests for the core PawPal+ classes."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_sets_completed_to_true() -> None:
    """A new task starts incomplete and is complete after mark_complete()."""
    task = Task("Morning walk", 30, "high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    """Adding a task to a pet adds it to that pet's task list."""
    pet = Pet("Biscuit", "dog")
    assert len(pet.tasks) == 0

    task = Task("Feeding", 10, "high")
    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


# --- Phase 4 features ---


def make_scheduler() -> Scheduler:
    """Return a Scheduler for a simple owner with no pets."""
    return Scheduler(Owner("Test Owner", available_minutes=60))


def test_sort_by_time_orders_tasks_earliest_first() -> None:
    """Tasks added out of order come back sorted by start time."""
    tasks = [
        Task("Dinner", 10, "high", time="18:00"),
        Task("Breakfast", 10, "high", time="07:30"),
        Task("Walk", 30, "medium", time="12:00"),
    ]

    sorted_tasks = make_scheduler().sort_by_time(tasks)

    assert [task.title for task in sorted_tasks] == ["Breakfast", "Walk", "Dinner"]


def test_sort_by_time_puts_tasks_without_time_last() -> None:
    """A task with no set time goes after all the timed tasks."""
    tasks = [
        Task("Brushing", 15, "low"),  # no time
        Task("Evening walk", 30, "high", time="19:00"),
        Task("Feeding", 10, "high", time="08:00"),
    ]

    sorted_tasks = make_scheduler().sort_by_time(tasks)

    assert [task.title for task in sorted_tasks] == ["Feeding", "Evening walk", "Brushing"]


def test_completing_daily_task_adds_copy_for_next_day() -> None:
    """Completing a daily task adds a new, unfinished copy due one day later."""
    pet = Pet("Biscuit", "dog")
    walk = Task("Morning walk", 30, "high", time="08:00", frequency="daily")
    pet.add_task(walk)

    next_walk = pet.complete_task(walk)

    assert walk.completed is True
    assert next_walk is not None
    assert next_walk.completed is False
    assert next_walk.due_date == walk.due_date + timedelta(days=1)
    assert next_walk.title == "Morning walk"
    assert next_walk.time == "08:00"
    assert len(pet.tasks) == 2


def test_completing_weekly_task_adds_copy_for_next_week() -> None:
    """Completing a weekly task adds a new copy due seven days later."""
    pet = Pet("Mochi", "cat")
    bath = Task("Bath", 20, "medium", frequency="weekly")
    pet.add_task(bath)

    next_bath = pet.complete_task(bath)

    assert next_bath is not None
    assert next_bath.due_date == bath.due_date + timedelta(days=7)
    assert len(pet.tasks) == 2


def test_completing_one_time_task_does_not_repeat() -> None:
    """A task that only happens once is marked done and no copy is added."""
    pet = Pet("Mochi", "cat")
    vet = Task("Vet visit", 60, "high")
    pet.add_task(vet)

    next_task = pet.complete_task(vet)

    assert vet.completed is True
    assert next_task is None
    assert len(pet.tasks) == 1


def test_next_daily_task_is_not_in_todays_plan() -> None:
    """After completing a daily task, tomorrow's copy is not scheduled today."""
    owner = Owner("Jordan", available_minutes=60)
    pet = Pet("Biscuit", "dog")
    owner.add_pet(pet)
    walk = Task("Morning walk", 30, "high", time="08:00", frequency="daily", due_date=date.today())
    pet.add_task(walk)

    pet.complete_task(walk)
    plan = Scheduler(owner).generate_plan()

    assert plan == []


def test_overlapping_tasks_are_flagged_as_conflict() -> None:
    """A 30-minute walk at 08:00 overlaps with medicine at 08:15."""
    tasks = [
        Task("Morning walk", 30, "high", time="08:00"),
        Task("Give medicine", 5, "high", time="08:15"),
    ]

    conflicts = make_scheduler().detect_conflicts(tasks)

    assert len(conflicts) == 1
    assert "Morning walk" in conflicts[0]
    assert "Give medicine" in conflicts[0]


def test_back_to_back_tasks_do_not_conflict() -> None:
    """A task starting exactly when another ends (08:00-08:30, then 08:30) is fine."""
    tasks = [
        Task("Morning walk", 30, "high", time="08:00"),
        Task("Feeding", 10, "high", time="08:30"),
    ]

    conflicts = make_scheduler().detect_conflicts(tasks)

    assert conflicts == []


def test_tasks_without_time_are_never_in_conflict() -> None:
    """Tasks with no set time are skipped by conflict detection."""
    tasks = [
        Task("Brushing", 15, "low"),
        Task("Play time", 20, "medium"),
        Task("Feeding", 10, "high", time="08:00"),
    ]

    conflicts = make_scheduler().detect_conflicts(tasks)

    assert conflicts == []
