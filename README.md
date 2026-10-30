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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
2 passed in 0.00s
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

**In the Streamlit app:** the task form now has a start time and a "Repeats" option; the task list can be filtered by pet and status and is sorted by time; a "Complete a Task" section marks tasks done (and schedules the next one for repeating tasks); and the generated schedule shows any time conflicts as warnings.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
