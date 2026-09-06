# Household Chore Manager

A small Django app for tracking household chores. It shows who's assigned
to each chore this period, lets people mark chores done, and rotates each
chore to the next person on a fixed cadence — so nobody is stuck with the
same chore every time and nothing quietly falls through the cracks. See
[_docs/plan.md](_docs/plan.md) for the full product plan and
[_docs/backlog.md](_docs/backlog.md) for implementation status.

## Requirements

- Python 3.x
- pip

## Setup

1. Create a virtual environment:

   ```
   python -m venv venv
   ```

2. Activate the virtual environment:

   ```
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```
   python manage.py migrate
   ```

5. (Optional) Create an admin user, to manage households/people/chores at `/admin/`:

   ```
   python manage.py createsuperuser
   ```

6. (Optional) Load example households, people, and chores:

   ```
   python manage.py seed_demo_data
   python manage.py rotate_chores
   ```

## Running the server

Activate the virtual environment first (`venv\Scripts\activate`), then:

```
python manage.py runserver
```

Then open:

- Dashboard: http://127.0.0.1:8000/
- Manage households: http://127.0.0.1:8000/households/
- Manage chores: http://127.0.0.1:8000/chores/
- Admin: http://127.0.0.1:8000/admin/

## Running tests

Activate the virtual environment first (`venv\Scripts\activate`), then:

```
python manage.py test
```

## Rotating chores

Each chore rotates to the next person in its configured order, and any
assignment still pending from the previous period is flagged as incomplete.
Activate the virtual environment first (`venv\Scripts\activate`), then run
it manually with:

```
python manage.py rotate_chores
```

To run it automatically on a fixed cadence (e.g. daily), schedule this
command with your OS scheduler:

- **Windows Task Scheduler**: create a task that runs
  `<path-to-venv>\Scripts\python.exe manage.py rotate_chores` with the
  working directory set to the project root.
- **cron** (Linux/macOS): add a line like
  `0 6 * * * cd /path/to/project && ./venv/bin/python manage.py rotate_chores`.
