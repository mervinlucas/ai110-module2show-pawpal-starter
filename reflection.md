# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
