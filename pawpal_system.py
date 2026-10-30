"""PawPal+ system classes: Owner, Pet, Task, and Scheduler."""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import Optional

# Turns a priority label into a number so tasks are easy to sort.
PRIORITY_VALUES = {"high": 3, "medium": 2, "low": 1}

# How many days until a recurring task comes back.
FREQUENCY_DAYS = {"daily": 1, "weekly": 7}


@dataclass
class Task:
    """A single pet care activity, like a walk or a feeding."""

    title: str
    duration_minutes: int
    priority: str  # "high", "medium", or "low"
    completed: bool = False
    time: str = ""  # start time as "HH:MM"; empty means no set time
    frequency: str = "once"  # "once", "daily", or "weekly"
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def priority_value(self) -> int:
        """Return the priority as a number (high=3, medium=2, low=1)."""
        return PRIORITY_VALUES.get(self.priority.lower(), 0)

    def start_minutes(self) -> Optional[int]:
        """Return the start time as minutes after midnight, or None if there is no set time."""
        if not self.time:
            return None
        hours, minutes = self.time.split(":")
        return int(hours) * 60 + int(minutes)

    def end_minutes(self) -> Optional[int]:
        """Return the end time as minutes after midnight, or None if there is no set time."""
        start = self.start_minutes()
        if start is None:
            return None
        return start + self.duration_minutes

    def next_occurrence(self) -> Optional["Task"]:
        """Return a fresh copy of this task for its next due date, or None if it doesn't repeat."""
        days = FREQUENCY_DAYS.get(self.frequency)
        if days is None:
            return None
        return replace(self, completed=False, due_date=self.due_date + timedelta(days=days))


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

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task done. If it repeats, add and return the next occurrence."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            self.add_task(next_task)
        return next_task


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

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by start time (earliest first). Tasks with no set time go last."""
        return sorted(tasks, key=lambda task: (task.time == "", task.time))

    def filter_tasks(
        self, pet_name: Optional[str] = None, completed: Optional[bool] = None
    ) -> list[Task]:
        """Return tasks for one pet and/or with one completion status. None means "any"."""
        results: list[Task] = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is None or task.completed == completed:
                    results.append(task)
        return results

    def generate_plan(self) -> list[Task]:
        """Pick tasks due today that fit in the owner's available time, then order them by time."""
        self.plan = []
        self.skipped = []
        time_left = self.owner.available_minutes

        # Only unfinished tasks that are due today (or overdue) need scheduling.
        tasks_to_do = [
            task
            for task in self.filter_tasks(completed=False)
            if task.due_date <= date.today()
        ]

        # Choose tasks by priority, so the most important ones get the time first.
        for task in self.sort_tasks(tasks_to_do):
            if task.duration_minutes <= time_left:
                self.plan.append(task)
                time_left -= task.duration_minutes
            else:
                self.skipped.append(task)

        # Show the chosen tasks in the order they happen during the day.
        self.plan = self.sort_by_time(self.plan)
        return self.plan

    def detect_conflicts(self, tasks: Optional[list[Task]] = None) -> list[str]:
        """Return a warning for each pair of tasks whose times overlap (defaults to the plan)."""
        if tasks is None:
            tasks = self.plan
        timed_tasks = [task for task in tasks if task.time]

        warnings: list[str] = []
        # Compare every pair of tasks once.
        for i in range(len(timed_tasks)):
            for j in range(i + 1, len(timed_tasks)):
                first, second = timed_tasks[i], timed_tasks[j]
                if first.start_minutes() < second.end_minutes() and second.start_minutes() < first.end_minutes():
                    warnings.append(
                        f"'{first.title}' at {first.time} overlaps with '{second.title}' at {second.time}."
                    )
        return warnings

    def explain_plan(self) -> str:
        """Return a readable explanation of what was planned and skipped."""
        lines: list[str] = []
        time_used = 0

        for task in self.plan:
            time_used += task.duration_minutes
            at_time = f" at {task.time}" if task.time else ""
            lines.append(
                f"Added '{task.title}'{at_time} ({task.priority} priority, {task.duration_minutes} min)."
            )

        for task in self.skipped:
            lines.append(
                f"Skipped '{task.title}' ({task.duration_minutes} min): not enough time left."
            )

        if not lines:
            return "No tasks to schedule."

        lines.append(f"Total time used: {time_used} of {self.owner.available_minutes} min.")
        return "\n".join(lines)
