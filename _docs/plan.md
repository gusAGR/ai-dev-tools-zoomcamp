# Household Chore Manager – Product Plan

## Problem Statement
Shared households lack visibility into who's responsible for chores and whether they've been completed. This leads to:
- People forgetting whose turn it is, causing chores to pile up or get done twice
- Unclear accountability—no one knows what's actually been done vs. what's pending
- Unfair distribution over time when assignments aren't tracked

## Product Goal
Build a simple, transparent chore assignment and tracking system that eliminates confusion about responsibility and completion, making shared households run smoother with less friction.

---

## Features

| # | Feature | Category | Description |
|---|---------|----------|---|
| 1 | View current assignments | MVP | **Dashboard shows each chore + person assigned this week.** At a glance, see who owns what. Person assignment is clear and non-negotiable. Reduces "whose turn is it?" questions. |
| 2 | Mark chore done | MVP | **Person clicks "Done" on their chore; it updates immediately.** Provides instant feedback that the task is complete. Creates accountability by recording who marked it done. Shows completion timestamp for clarity. |
| 3 | Auto-rotate on fixed day | MVP | **Every [day/time], system shifts each chore to next person in cycle.** Happens automatically without manual intervention. Ensures fair distribution over time. Prevents the same person from always doing the same chore. |
| 4 | Flag incomplete chores | MVP | **Chores not marked done by rotation day stay visible as "Incomplete".** Overdue tasks don't disappear—they stay flagged for visibility. Helps identify blockers or accountability issues. Prevents swept-under-the-rug scenarios. |
| 5 | Manage household | MVP | **Add/remove people from household; controls who's in the rotation pool.** Adapts to household changes (guests leaving, new roommate arriving). Determines who participates in the rotation cycle. Keeps the system current and relevant. |
| 6 | Manage chore list | MVP | **Define which chores exist and how many people rotate through each.** Allows customization of the fixed chore set per household. Controls rotation pool size (e.g., dishes rotates among 3 people, laundry among 2). Scope of work is clearly defined. |
| 7 | Completion history | Add-on | **View past 4-8 weeks: who did what, when they marked it done.** Tracks trends over time—see if chores are consistently late or early. Provides data for fairness discussions. Useful for spotting recurring problems. |
| 8 | Fairness view | Add-on | **Total chores completed per person over time; spot if someone's doing less.** Quantifies whether the rotation is actually balanced. Surfaces inequities before resentment builds. Data-driven way to adjust assignments if needed. |
| 9 | Notes on incompletion | Add-on | **Optional reason why a chore wasn't done (sick, forgot, etc.).** Provides context instead of silent failure. Prevents assumptions about laziness or negligence. Helps household members understand blockers. |
| 10 | Skip/reassign current week | Add-on | **Temporarily move a chore to someone else this week (one-off change).** Handles life events without breaking the rotation system. Flexibility when someone is sick, traveling, or swamped. Doesn't permanently alter the cycle. |

---

## Required Features (Your Version)
*To be determined: Which features (1–10) are required for launch?*
