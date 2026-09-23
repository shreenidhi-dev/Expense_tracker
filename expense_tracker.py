"""
Expense Tracker - Python Mini Project
--------------------------------------
Features:
1. Add an expense (amount, category, date, note)
2. View all expenses
3. Filter expenses by category or date range
4. View summary (total spend, category-wise breakdown)
5. Visualize spending with charts (pie + bar)

Data is stored in expenses.csv in the same folder as this script.
"""

import csv
import os
from datetime import datetime

import matplotlib.pyplot as plt

CSV_FILE = "expenses.csv"
FIELDNAMES = ["date", "category", "amount", "note"]


# ---------- Data handling ----------

def init_csv():
    """Create the CSV file with headers if it doesn't exist yet."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_expenses():
    with open(CSV_FILE, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_expense(entry):
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(entry)


# ---------- Core features ----------

def add_expense():
    print("\n--- Add New Expense ---")
    date_str = input("Date (YYYY-MM-DD) [leave blank for today]: ").strip()
    if not date_str:
        date_str = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Expense not saved.")
            return

    category = input("Category (e.g., Food, Travel, Rent): ").strip().title()
    if not category:
        category = "Uncategorized"

    try:
        amount = float(input("Amount: ").strip())
    except ValueError:
        print("Invalid amount. Expense not saved.")
        return

    note = input("Note (optional): ").strip()

    entry = {"date": date_str, "category": category, "amount": amount, "note": note}
    save_expense(entry)
    print("Expense added successfully!\n")


def view_expenses(expenses=None):
    if expenses is None:
        expenses = load_expenses()

    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    print("\n{:<12} {:<15} {:>10}  {}".format("Date", "Category", "Amount", "Note"))
    print("-" * 55)
    for e in expenses:
        print("{:<12} {:<15} {:>10.2f}  {}".format(
            e["date"], e["category"], float(e["amount"]), e["note"]))
    print()


def filter_expenses():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    print("\n--- Filter Expenses ---")
    print("1. By category")
    print("2. By date range")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        category = input("Enter category: ").strip().title()
        filtered = [e for e in expenses if e["category"] == category]
    elif choice == "2":
        start = input("Start date (YYYY-MM-DD): ").strip()
        end = input("End date (YYYY-MM-DD): ").strip()
        try:
            start_dt = datetime.strptime(start, "%Y-%m-%d")
            end_dt = datetime.strptime(end, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format.")
            return
        filtered = [
            e for e in expenses
            if start_dt <= datetime.strptime(e["date"], "%Y-%m-%d") <= end_dt
        ]
    else:
        print("Invalid choice.")
        return

    view_expenses(filtered)


def show_summary():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    total = sum(float(e["amount"]) for e in expenses)
    category_totals = {}
    for e in expenses:
        category_totals[e["category"]] = category_totals.get(e["category"], 0) + float(e["amount"])

    print("\n--- Summary ---")
    print(f"Total spent: {total:.2f}")
    print("\nBy category:")
    for cat, amt in sorted(category_totals.items(), key=lambda x: -x[1]):
        pct = (amt / total) * 100
        print(f"  {cat:<15} {amt:>10.2f}  ({pct:.1f}%)")
    print()


def visualize_expenses():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    category_totals = {}
    for e in expenses:
        category_totals[e["category"]] = category_totals.get(e["category"], 0) + float(e["amount"])

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Pie chart
    axes[0].pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    axes[0].set_title("Spending by Category")

    # Bar chart
    axes[1].bar(categories, amounts, color="steelblue")
    axes[1].set_title("Category-wise Spend")
    axes[1].set_ylabel("Amount")
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    output_path = "expense_chart.png"
    plt.savefig(output_path)
    print(f"\nChart saved as '{output_path}'. Opening it now...\n")
    plt.show()


# ---------- Menu ----------

def main_menu():
    init_csv()
    while True:
        print("=" * 40)
        print("       EXPENSE TRACKER")
        print("=" * 40)
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Filter expenses")
        print("4. Show summary")
        print("5. Visualize spending (charts)")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            visualize_expenses()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    main_menu()
