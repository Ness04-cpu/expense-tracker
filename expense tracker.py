"""
Personal Expense Tracker
-------------------------
A small command-line app that stores expenses in a local SQLite database.

Why this project is a good learning piece:
- Uses SQL (CREATE TABLE, INSERT, SELECT, SUM) with Python's built-in sqlite3
- Has a simple menu loop, which is a common beginner CLI pattern
- Is easy to extend (see IDEAS.md for next steps you can add yourself)
"""

import sqlite3
from datetime import date
import CSV

DB_NAME = "expenses.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL
        )
    """)
    return conn


def add_expense(conn):
    entry_date = input("Date (YYYY-MM-DD, blank = today): ").strip() or str(date.today())
    category = input("Category (e.g. food, transport, school): ").strip()
    description = input("Description: ").strip()
    amount_str = input("Amount: ").strip()

    try:
        amount = float(amount_str)
    except ValueError:
        print("Amount must be a number. Expense not saved.")
        return

    conn.execute(
        "INSERT INTO expenses (entry_date, category, description, amount) VALUES (?, ?, ?, ?)",
        (entry_date, category, description, amount),
    )
    conn.commit()
    print("Expense added.\n")


def list_expenses(conn):
    rows = conn.execute(
        "SELECT id, entry_date, category, description, amount FROM expenses ORDER BY entry_date DESC"
    ).fetchall()

    if not rows:
        print("No expenses recorded yet.\n")
        return

    print(f"\n{'ID':<4}{'Date':<12}{'Category':<15}{'Description':<20}{'Amount':>10}")
    print("-" * 61)
    for row in rows:
        print(f"{row[0]:<4}{row[1]:<12}{row[2]:<15}{row[3]:<20}{row[4]:>10.2f}")
    print()

def export_to_csv(conn):
    filename = input("Filename to save as (e.g. expenses.csv): ").strip()
    if not filename:
        filename = "expenses_export.csv"
    if not filename.endswith(".csv"):
        filename += ".csv"

    rows = conn.execute(
        "SELECT entry_date, category, description, amount FROM expenses ORDER BY entry_date"
    ).fetchall()

    if not rows:
        print("No expenses to export.\n")
        return

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Description", "Amount"])  # header row
        writer.writerows(rows)

    print(f"Exported {len(rows)} expenses to {filename}\n")


def total_by_category(conn):
    rows = conn.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC"
    ).fetchall()

    if not rows:
        print("No expenses recorded yet.\n")
        return

    print("\nTotal spent by category:")
    for category, total in rows:
        print(f"  {category:<20}{total:>10.2f}")
    print()


def delete_expense(conn):
    list_expenses(conn)
    id_str = input("Enter the ID of the expense to delete: ").strip()
    try:
        expense_id = int(id_str)
    except ValueError:
        print("Invalid ID.\n")
        return

    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    print("Deleted (if that ID existed).\n")


def main():
    conn = connect()
    menu = """
Personal Expense Tracker
1. Add expense
2. List all expenses
3. Totals by category
4. Delete an expense
5. Export to CSV
6. Quit
"""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(conn)
        elif choice == "2":
            list_expenses(conn)
        elif choice == "3":
            total_by_category(conn)
        elif choice == "4":
            delete_expense(conn)
        elif choice == "5":
            export_to_csv(conn)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Not a valid option, try again.\n")

    conn.close()


if __name__ == "__main__":
    main()
