# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Django app (project `choremanager`, app `chores`) for tracking household
chores: it shows who's assigned to each chore this period, lets people mark
chores done, and rotates each chore to the next person on a fixed cadence.
See [_docs/plan.md](_docs/plan.md) for the product plan and
[_docs/backlog.md](_docs/backlog.md) for what's implemented vs. pending.

There is currently no authentication — all households/chores are visible
and editable by anyone who can reach the app.

## Commands

Activate the virtual environment first (`venv\Scripts\activate`), then:

```
python manage.py runserver          # dev server at :8000
python manage.py test                # full test suite
python manage.py test chores.tests.MarkDoneViewTests   # one test class
python manage.py test chores.tests.MarkDoneViewTests.test_mark_done_requires_post  # one test
python manage.py makemigrations chores   # after model changes
python manage.py migrate
python manage.py rotate_chores        # advance rotations, flag incomplete
python manage.py seed_demo_data        # load example households/chores
```

After adding a dependency, refresh `requirements.txt` with
`pip freeze > requirements.txt`.

## Architecture

Everything lives in the single `chores` app; there is no split into
multiple apps.

**Data model** ([chores/models.py](chores/models.py)):
- `Household` has many `Person`.
- `Chore` belongs to a `Household` and has a rotation order of people via
  the `ChoreRotation` through-model (`chore`, `person`, `order`).
- `ChoreAssignment` is a materialized record — one per chore per period —
  with `status` (`pending`/`done`/`incomplete`) and `completed_at`. The
  dashboard and rotation logic both work off this table, not the
  `ChoreRotation` order directly.

**Rotation logic** ([chores/management/commands/rotate_chores.py](chores/management/commands/rotate_chores.py)):
This is the core domain logic, meant to run on a schedule (see README's
"Rotating chores" section for cron/Task Scheduler wiring — nothing is
scheduled automatically). For each chore, it looks at the most recent
`ChoreAssignment`: if still `pending`, it's flagged `incomplete`; then a new
`ChoreAssignment` is created for today's date, assigned to whoever comes
next after the last-assigned person in that chore's `ChoreRotation` order
(wrapping around). Chores with no rotation configured are skipped. Running
it twice on the same day is a no-op (checks `period_start == today`).

**Views** ([chores/views.py](chores/views.py)) are plain function-based
views, no forms/DRF — each reads `request.POST` directly and redirects
back to the relevant list/detail page. Mutating views (`mark_done`,
`person_delete`, `chore_delete`, `rotation_delete`) only act on POST and
redirect on GET. `django.contrib.messages` is used for one-off feedback,
rendered in [chores/templates/chores/_base.html](chores/templates/chores/_base.html)
which all other templates extend.

**Dashboard view** computes "current" assignments in Python (not SQL):
it pulls all `ChoreAssignment`s ordered by `chore_id, -period_start` and
takes the first one seen per `chore_id`, i.e. the latest by period.

## Testing conventions

Tests live in [chores/tests.py](chores/tests.py) as `TestCase` subclasses
grouped by feature (rotation command, mark-done view, household views,
chore views). Rotation tests call the management command directly via
`call_command("rotate_chores")` and manipulate `period_start` with
`timedelta` to simulate the passage of a period, rather than mocking time.
