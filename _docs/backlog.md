# Backlog — Household Chore Manager

Derived from [_docs/plan.md](_docs/plan.md). Scoped to the MVP features (1–6); add-ons (7–10) are listed at the bottom for later.

## MVP

- [x] **Household & Person models** — `chores` app models for `Household` and `Person` (name, household FK). Supports "Manage household" (feature 5).
- [x] **Chore & rotation models** — `Chore` model (name, household FK, rotation order/list of people) and `ChoreAssignment` model (chore FK, person FK, week/period, status: pending/done/incomplete, completed_at timestamp). Supports "Manage chore list" (feature 6).
- [x] **Admin registration** — register `Household`, `Person`, `Chore`, `ChoreAssignment` in `chores/admin.py` so data can be managed before UI exists.
- [x] **Dashboard view** — view + template listing current-week `ChoreAssignment`s per household, showing chore + assigned person. Implements "View current assignments" (feature 1).
- [x] **Mark chore done** — view/endpoint (e.g. POST from dashboard) that sets a `ChoreAssignment` to done and records `completed_at` + who completed it. Implements feature 2.
- [x] **Rotation command** — management command (`manage.py rotate_chores`) that advances each chore to the next person in the household's rotation and creates the new period's `ChoreAssignment`s. Implements "Auto-rotate on fixed day" (feature 3).
- [x] **Schedule the rotation** — documented in README how to wire `rotate_chores` into Windows Task Scheduler or cron; not registered on this machine (would modify system state outside the repo).
- [x] **Incomplete flagging** — folded into the rotation command: any assignment still pending from the previous period is marked "incomplete" before the next one is created. Implements feature 4.
- [x] **Manage household UI** — views/forms at `/households/` and `/households/<id>/` to create households and add/remove people. Implements feature 5.
- [x] **Manage chore list UI** — views/forms at `/chores/` and `/chores/<id>/` to create chores and manage rotation order. Implements feature 6.
- [ ] **Auth / household scoping** — basic login so each person only sees/acts on their own household's data (needed before "Manage household" and "Mark chore done" are meaningful with multiple households). *Deferred — not implementing login per current instructions.*

## Add-ons (later)

- [ ] Completion history view (past 4–8 weeks per household) — feature 7.
- [ ] Fairness view (totals per person over time) — feature 8.
- [ ] Notes on incompletion (optional reason field on `ChoreAssignment`) — feature 9.
- [ ] Skip/reassign current week (one-off override without changing the rotation cycle) — feature 10.
