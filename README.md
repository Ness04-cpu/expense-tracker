# Personal Expense Tracker

A simple command-line app for tracking personal expenses, built with Python and SQLite.

## What it does

- Add an expense (date, category, description, amount)
- List all expenses, most recent first
- See totals grouped by category
- Delete an expense by ID

Data is stored locally in an `expenses.db` SQLite file (created automatically the first time you run it).

## How to run it

You need Python 3 installed (no extra packages required — `sqlite3` is built in).

```bash
python3 tracker.py
```

Then follow the on-screen menu.

## Why I built this

I'm a Computer Science / IT student learning Python and SQL, and wanted a small project
that actually uses a real database instead of just printing to the screen. This shows
basic CRUD operations (Create, Read, Update, Delete) against a SQLite table.

## What I'd like to add next

- [ ] Edit an existing expense instead of only delete/re-add
- [ ] Filter expenses by date range
- [ ] Export expenses to a CSV file
- [ ] Add a monthly budget limit per category and warn when exceeded
- [ ] Build a simple web front-end for this using Flask + HTML/CSS
