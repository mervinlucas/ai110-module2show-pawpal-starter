"""Tests for the core PawPal+ classes."""

from pawpal_system import Pet, Task


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
