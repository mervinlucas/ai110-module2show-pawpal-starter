"""PawPal+ system classes: Owner, Pet, Task, and Scheduler."""

from dataclasses import dataclass, field

# Turns a priority label into a number so tasks are easy to sort.
PRIORITY_VALUES = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    """A single pet care activity, like a walk or a feeding."""

    title: str
    duration_minutes: int
    priority: str  # "high", "medium", or "low"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def priority_value(self) -> int:
        """Return the priority as a number (high=3, medium=2, low=1)."""
        return PRIORITY_VALUES.get(self.priority.lower(), 0)


@dataclass
class Pet:
    """A pet and its list of care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove a task by its title."""
        self.tasks = [task for task in self.tasks if task.title != title]


class Owner:
    """The pet owner, their pets, and how much time they have today."""

    def __init__(self, name: str, available_minutes: int) -> None:
        self.name: str = name
        self.available_minutes: int = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task from every pet."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """Builds a daily care plan for an owner based on priority and time."""

    def __init__(self, owner: Owner) -> None:
        self.owner: Owner = owner
        self.plan: list[Task] = []
        self.skipped: list[Task] = []

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority (highest first), then by shortest duration."""
        return sorted(tasks, key=lambda task: (-task.priority_value(), task.duration_minutes))

    def generate_plan(self) -> list[Task]:
        """Pick tasks that fit in the owner's available time."""
        self.plan = []
        self.skipped = []
        time_left = self.owner.available_minutes

        # Completed tasks don't need to be scheduled again.
        tasks_to_do = [task for task in self.owner.get_all_tasks() if not task.completed]

        for task in self.sort_tasks(tasks_to_do):
            if task.duration_minutes <= time_left:
                self.plan.append(task)
                time_left -= task.duration_minutes
            else:
                self.skipped.append(task)

        return self.plan

    def explain_plan(self) -> str:
        """Return a readable explanation of what was planned and skipped."""
        lines: list[str] = []
        time_used = 0

        for task in self.plan:
            time_used += task.duration_minutes
            lines.append(
                f"Added '{task.title}' ({task.priority} priority, {task.duration_minutes} min)."
            )

        for task in self.skipped:
            lines.append(
                f"Skipped '{task.title}' ({task.duration_minutes} min): not enough time left."
            )

        if not lines:
            return "No tasks to schedule."

        lines.append(f"Total time used: {time_used} of {self.owner.available_minutes} min.")
        return "\n".join(lines)
