"""
main.py - Entry point for Smart Expense Tracker
Run: python main.py
"""
from database import initialize_db
from expense import Expense
from expense_manager import ExpenseManager
from display import (
    show_main_menu, show_expenses, show_category_summary,
    show_monthly_summary, header, success, error, info,
    show_categories, divider,
)
from datetime import datetime


manager = ExpenseManager()


# ──────────────────────────────────────────────────────────
# ADD
# ──────────────────────────────────────────────────────────

def add_expense():
    header("Add New Expense")
    try:
        amount_str = input("  Amount (₹): ").strip()
        amount = Expense.validate_amount(amount_str)

        show_categories()
        choice = input("\n  Choose category (number): ").strip()
        category = Expense.validate_category(choice)

        description = input("  Description: ").strip()
        if not description:
            raise ValueError("Description cannot be empty.")

        date_input = input("  Date (YYYY-MM-DD) [leave blank for today]: ").strip()
        if date_input:
            datetime.strptime(date_input, "%Y-%m-%d")  # validate format
        else:
            date_input = datetime.now().strftime("%Y-%m-%d")

        expense = Expense(amount, category, description, date_input)
        new_id = manager.add_expense(expense)
        success(f"Expense added! ID: {new_id}  |  ₹{amount:.2f}  |  {category}")

    except ValueError as e:
        error(str(e))


# ──────────────────────────────────────────────────────────
# VIEW ALL
# ──────────────────────────────────────────────────────────

def view_all():
    expenses = manager.get_all_expenses()
    show_expenses(expenses, "All Expenses")


# ──────────────────────────────────────────────────────────
# VIEW BY CATEGORY
# ──────────────────────────────────────────────────────────

def view_by_category():
    show_categories()
    choice = input("\n  Choose category (number): ").strip()
    try:
        category = Expense.validate_category(choice)
        expenses = manager.get_expenses_by_category(category)
        show_expenses(expenses, f"Expenses — {category}")
    except ValueError as e:
        error(str(e))


# ──────────────────────────────────────────────────────────
# VIEW BY MONTH
# ──────────────────────────────────────────────────────────

def view_by_month():
    header("View by Month")
    now = datetime.now()
    year_str = input(f"  Year [{now.year}]: ").strip() or str(now.year)
    month_str = input(f"  Month (1-12) [{now.month}]: ").strip() or str(now.month)
    try:
        year, month = int(year_str), int(month_str)
        if not (1 <= month <= 12):
            raise ValueError("Month must be 1–12.")
        expenses = manager.get_expenses_by_month(year, month)
        show_expenses(expenses, f"Expenses — {year}-{month:02d}")
    except ValueError as e:
        error(str(e))


# ──────────────────────────────────────────────────────────
# ANALYTICS
# ──────────────────────────────────────────────────────────

def show_analytics():
    header("Analytics & Summary")
    expenses = manager.get_all_expenses()

    if not expenses:
        info("No expenses recorded yet.")
        return

    total = manager.get_total(expenses)
    avg = manager.get_average_expense(expenses)
    highest = manager.get_highest_expense(expenses)
    summary = manager.get_summary_by_category(expenses)
    monthly = manager.get_monthly_summary()

    print(f"\n  Total Expenses   : ₹{total:.2f}")
    print(f"  Total Records    : {len(expenses)}")
    print(f"  Average per Entry: ₹{avg:.2f}")
    if highest:
        print(f"  Highest Expense  : ₹{highest.amount:.2f} ({highest.description})")

    print()
    show_category_summary(summary, total)
    print()
    show_monthly_summary(monthly)


# ──────────────────────────────────────────────────────────
# EDIT
# ──────────────────────────────────────────────────────────

def edit_expense():
    header("Edit Expense")
    try:
        exp_id = int(input("  Enter Expense ID to edit: ").strip())
        expense = manager.get_expense_by_id(exp_id)
        if not expense:
            error(f"No expense found with ID {exp_id}.")
            return

        print(f"\n  Current: {expense}")
        print("  (Press Enter to keep current value)\n")

        amount_str = input(f"  New Amount [₹{expense.amount}]: ").strip()
        if amount_str:
            expense.amount = Expense.validate_amount(amount_str)

        show_categories()
        choice = input(f"\n  New Category [current: {expense.category}]: ").strip()
        if choice:
            expense.category = Expense.validate_category(choice)

        desc = input(f"  New Description [{expense.description}]: ").strip()
        if desc:
            expense.description = desc

        date_str = input(f"  New Date [{expense.date}]: ").strip()
        if date_str:
            datetime.strptime(date_str, "%Y-%m-%d")
            expense.date = date_str

        if manager.update_expense(expense):
            success("Expense updated successfully.")
        else:
            error("Update failed.")

    except ValueError as e:
        error(str(e))


# ──────────────────────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────────────────────

def delete_expense():
    header("Delete Expense")
    try:
        exp_id = int(input("  Enter Expense ID to delete: ").strip())
        expense = manager.get_expense_by_id(exp_id)
        if not expense:
            error(f"No expense found with ID {exp_id}.")
            return

        print(f"\n  → {expense}")
        confirm = input("\n  Confirm delete? (yes/no): ").strip().lower()
        if confirm == "yes":
            if manager.delete_expense(exp_id):
                success("Expense deleted.")
            else:
                error("Could not delete.")
        else:
            info("Deletion cancelled.")

    except ValueError as e:
        error(str(e))


# ──────────────────────────────────────────────────────────
# MAIN LOOP
# ──────────────────────────────────────────────────────────

MENU_ACTIONS = {
    "1": add_expense,
    "2": view_all,
    "3": view_by_category,
    "4": view_by_month,
    "5": show_analytics,
    "6": edit_expense,
    "7": delete_expense,
}


def main():
    print("\n  Initializing Smart Expense Tracker...")
    initialize_db()

    while True:
        show_main_menu()
        choice = input("  Enter option: ").strip()

        if choice == "0":
            print("\n  Goodbye! 👋\n")
            break
        elif choice in MENU_ACTIONS:
            MENU_ACTIONS[choice]()
        else:
            print("  Invalid option. Try again.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()