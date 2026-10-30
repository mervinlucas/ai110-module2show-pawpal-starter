"""PawPal+ system classes: Owner, Pet, Task, and Scheduler."""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity, like a walk or a feeding."""

    title: str
    duration_minutes: int
    priority: str  # "high", "medium", or "low"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass

    def priority_value(self) -> int:
        """Return the priority as a number (high=3, medium=2, low=1)."""
        pass


@dataclass
class Pet:
    """A pet and its list of care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, title: str) -> None:
        """Remove a task by its title."""
        pass


class Owner:
    """The pet owner, their pets, and how much time they have today."""

    def __init__(self, name: str, available_minutes: int) -> None:
        self.name: str = name
        self.available_minutes: int = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return every task from every pet."""
        pass


class Scheduler:
    """Builds a daily care plan for an owner based on priority and time."""

    def __init__(self, owner: Owner) -> None:
        self.owner: Owner = owner
        self.plan: list[Task] = []
        self.skipped: list[Task] = []

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority (highest first), then by shortest duration."""
        pass

    def generate_plan(self) -> list[Task]:
        """Pick tasks that fit in the owner's available time."""
        pass

    def explain_plan(self) -> str:
        """Return a readable explanation of what was planned and skipped."""
        pass
