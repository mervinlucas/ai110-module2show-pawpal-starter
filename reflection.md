# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My first UML had four classes: `Owner`, `Pet`, `Task`, and `Scheduler`. The relationships were simple. An Owner has many Pets, a Pet has many Tasks, and the Scheduler works with one Owner to build the plan.

- **Task** just holds data about one care activity (title, duration, priority, done or not). It has two small helpers, `mark_complete()` and `priority_value()`, which turns "high/medium/low" into 3/2/1 so tasks are easy to sort.
- **Pet** holds a name, species, and its list of tasks, with `add_task()` and `remove_task()`.
- **Owner** holds the owner's name, how many minutes they have today, and their pets. `get_all_tasks()` collects every task from every pet into one list.
- **Scheduler** is where all the actual decisions happen: sorting tasks, building the plan, and explaining it.

I wanted the "thinking" to be in one place (the Scheduler) and the other classes to mostly just store things. That made it a lot easier to know where to look when something was wrong, and it meant my tests could focus on the Scheduler.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. The four classes and their relationships never changed, but each class grew a bit in Phase 4:

- `Task` got three new fields: `time` (like `"08:00"`), `frequency` (`once`, `daily`, `weekly`), and `due_date`. I gave all of them default values so my old code, tests, and CLI demo still worked without changes.
- `Pet` got `complete_task()`. My first thought was to put the recurring logic inside `Task.mark_complete()`, but a Task doesn't know which pet it belongs to, so it couldn't add the next copy to the list. Putting it on `Pet` made more sense because the pet owns the task list. `Task` still creates the copy (`next_occurrence()`), and `Pet` adds it.
- `Scheduler` got `sort_by_time()`, `filter_tasks()`, and `detect_conflicts()`. I also changed `generate_plan()` so it still *chooses* tasks by priority but *shows* them in time order, because a schedule that isn't in time order is confusing to read.

I updated `diagrams/uml.mmd` at the end so it matches the final code.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler looks at:

1. **Available time.** It never plans more minutes than the owner said they have.
2. **Priority.** High-priority tasks get the time first.
3. **Duration.** If two tasks have the same priority, the shorter one goes first so more tasks fit.
4. **Completion and due date.** Tasks that are already done, or not due until a later day (like tomorrow's copy of a daily walk), are left out.
5. **Start times.** These are used to order the plan and to check for overlaps.

I decided time and priority mattered most because those are the two things a busy owner actually has to trade off. Things like medicine and feeding can't be skipped, but brushing can wait a day. Start times are a softer constraint. I use them to warn about conflicts, but I don't let them decide what gets dropped.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler picks tasks **greedily by priority**. It sorts tasks from high to low priority (shortest first when priorities tie) and adds each one if it still fits in the owner's available time. It does not search every possible combination for the "best" use of time. As a result, a lower-priority task can sometimes beat a higher-priority one. In my demo, "Play time" (medium, 20 min) was skipped but "Brushing" (low, 15 min) was added, because only 15 minutes were left after the high-priority tasks. Checking every combination would fill time a little better in some cases, but the number of combinations grows very quickly. That approach would also be harder to explain to the owner. With the greedy approach, the most important tasks (meds, feeding) are always considered first, and `explain_plan()` can give a simple reason for every decision.

A second tradeoff is in **conflict detection**. `detect_conflicts()` compares every pair of timed tasks, which takes about n² checks. Sorting by start time first and only comparing neighbors would be faster. But an owner will only have a handful of tasks per day, so the speed difference doesn't matter here, and the nested loop is easier to read and test. Conflicts are also only **warnings**: the scheduler doesn't move tasks around automatically. An owner might really be able to give meds during a walk, so I decided they should make that call rather than the app.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Claude Code (in VS Code) for pretty much every phase: brainstorming the four classes, turning that into a Mermaid UML diagram, generating class skeletons, filling in the logic, wiring up the Streamlit UI, adding the Phase 4 features, and writing tests.

I treated it like a separate, focused request for each phase instead of one huge "build my whole app" prompt. Each request only had one job (design, then skeletons, then logic, then UI, and so on), and I ended almost all of them with "don't start the next phase yet." That helped a lot. Each step was small enough that I could actually read what changed, run it, and commit it before moving on (my git history has one commit per phase). When I started a new phase, I pointed it at the files that already existed (like "use my `diagrams/uml.mmd`") so it built on what I had instead of inventing a new design.

The most helpful prompts were the ones with clear limits, like "keep it beginner-friendly," "don't change the existing class design," "don't modify any Python files," and "run the tests and tell me how you checked it." Asking for a summary of what files changed and how it was tested at the end of each phase was really useful, because it made me double check things instead of just trusting it.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The clearest one was the UML file. When I asked for Mermaid code to save as a `.mmd` file, the AI's answer was wrapped in markdown code fences (```` ```mermaid ````). I saved it like that at first, but those lines aren't valid in a `.mmd` file, so the diagram wouldn't render. I took them out myself so the file starts with `classDiagram`. The AI did point it out later too, but it was a good reminder that "looks right in chat" isn't the same as "works as a file."

Another one was in the Streamlit UI. The first version passed the actual `Pet` objects into the "choose a pet" dropdown. It said "Added 'Feeding' for Mochi" but the task never showed up, because Streamlit handed back a *copy* of the pet. It got caught because I'd asked for the app to be tested, not just written. The fix changed the design a little: the dropdown now uses pet names, which means **pet names have to be unique**, so the app now warns you if you try to add a second pet with the same name. I was fine with that tradeoff since two pets with the exact same name would be confusing anyway.

I also didn't just go along with everything it suggested adding. In the first design answer it mentioned ideas like a task `category`. I left that out because nothing in the assignment needed it.

For verifying, I mostly ran things: `python main.py` to see real output, `pytest` after every change, and actually clicking through the app. I also checked that the UML method and attribute names matched the code.

**How separate AI sessions/requests helped, and my role as lead architect**

Splitting the work into separate phase-by-phase requests kept the AI from "running ahead." It never rewrote the scheduler while I was asking about the UI, for example. I was the one deciding what the system should be: which four classes, that the Scheduler holds all the decisions, that conflicts are warnings and not automatic fixes, that completed tasks are left out of the plan, and what was in or out of scope for each phase. The AI was really fast at writing the code once I'd decided that, but I still had to read it, run it, and say no or "change this" when something didn't fit. I think of it like I was the architect and it was a fast builder that still needed someone checking the work.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I have 11 pytest tests in `tests/test_pawpal.py`:

- **Basics:** `mark_complete()` sets `completed` to `True`, and `add_task()` actually adds the task to the pet.
- **Sorting by time:** tasks come back earliest first, and a task with no time goes to the end instead of crashing or jumping to the front.
- **Recurring tasks:** completing a daily task adds a new unfinished copy due 1 day later. Weekly adds one due 7 days later. A one-time task doesn't add anything. Tomorrow's copy does *not* end up in today's plan.
- **Conflicts:** a 30-minute walk at 08:00 and meds at 08:15 get flagged, but back-to-back tasks (08:00–08:30, then 08:30) don't. Tasks without a time are never flagged.

These felt important because they're the parts that are easy to get *almost* right. The back-to-back test is a good example: if I'd used `<=` instead of `<` in the overlap check, every back-to-back pair would show a fake warning. The "not in today's plan" test checks that recurring tasks and the scheduler actually work together, not just separately.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm pretty confident for normal use. All the tests pass, the CLI output matches what I expect by hand, and I clicked through the whole app flow (add pets, add tasks, filter, sort, complete a task, generate the schedule with and without a conflict). I'd say about 4 out of 5.

Edge cases I'd test next:

- **An overdue daily task.** If a daily task from 3 days ago gets completed, the next copy is due 2 days ago, which is still "due," so it shows up again today. That might be fine or might be annoying, and I'd want to decide on purpose.
- **`remove_task()` with recurring tasks.** It removes by title, so it would remove *all* copies of "Morning walk," not just one.
- **Bad time strings in code** like `"8am"`. The app uses a time picker so it can't happen there, but `main.py` or tests could pass one in and `start_minutes()` would crash.
- Tasks that go past midnight, an owner with 0 minutes available, and a task that's longer than all the available time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most happy with how the backend and the UI stayed separate. All the logic lives in `pawpal_system.py`, and both `main.py` and the Streamlit app just call it. So when I added sorting, filtering, recurring tasks, and conflicts in Phase 4, I didn't have to write that logic twice. I also like that the app explains *why* it made the plan, instead of just showing a list.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

- Give each task an ID (or keep a link to its pet) so I don't have to rely on unique pet names and titles. That would fix the duplicate-name limitation and the `remove_task()` issue.
- Let the scheduler use start times as a real constraint, like suggesting a new time when two tasks overlap, instead of only warning.
- Save the data to a file so pets and tasks aren't lost when the Streamlit app restarts.
- Add tests for the edge cases listed above, plus a couple of tests for `filter_tasks()` and `generate_plan()` directly.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Doing the design (UML and class skeletons) *before* writing logic made working with AI way easier. Once I had a clear design, I could give the AI small, specific jobs and check each one against the design. When I gave clear limits it stayed on track, and when I asked it to actually run and test things, it caught real bugs (like the Pet dropdown one). The AI writes code fast, but deciding what to build, and checking that it really works, was still my job.
