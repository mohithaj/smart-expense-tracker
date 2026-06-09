"""
display.py - All terminal output / formatting helpers
"""
from expense import Expense


WIDTH = 65


def header(title: str):
    print("\n" + "═" * WIDTH)
    print(f"  {title}")
    print("═" * WIDTH)


def divider():
    print("─" * WIDTH)


def success(msg: str):
    print(f"\n  ✅  {msg}")


def error(msg: str):
    print(f"\n  ❌  {msg}")


def info(msg: str):
    print(f"  ℹ  {msg}")


def show_categories():
    print("\n  Categories:")
    for i, cat in enumerate(Expense.CATEGORIES, 1):
        print(f"    {i:2}. {cat}")


def show_expenses(expenses: list[Expense], title: str = "Expenses"):
    header(title)
    if not expenses:
        info("No expenses found.")
        return
    print(f"  {'ID':<5} {'Date':<12} {'Category':<20} {'Amount':>10}  Description")
    divider()
    for e in expenses:
        print(
            f"  {str(e.id):<5} {e.date:<12} {e.category:<20} "
            f"₹{e.amount:>8.2f}  {e.description}"
        )
    divider()
    total = sum(ex.amount for ex in expenses)
    print(f"  {'Total:':>40} ₹{total:>8.2f}")


def show_category_summary(summary: dict[str, float], total: float):
    header("Spending by Category")
    if not summary:
        info("No data.")
        return
    bar_max = 30
    max_val = max(summary.values()) if summary else 1
    print(f"  {'Category':<22} {'Amount':>10}   {'Bar'}")
    divider()
    for cat, amt in summary.items():
        bar_len = int((amt / max_val) * bar_max)
        bar = "█" * bar_len
        pct = (amt / total * 100) if total else 0
        print(f"  {cat:<22} ₹{amt:>8.2f}  {bar} {pct:.1f}%")
    divider()
    print(f"  {'TOTAL':<22} ₹{total:>8.2f}")


def show_monthly_summary(monthly: dict[str, float]):
    header("Monthly Summary")
    if not monthly:
        info("No data.")
        return
    print(f"  {'Month':<12} {'Total':>12}")
    divider()
    for month, total in monthly.items():
        print(f"  {month:<12} ₹{total:>10.2f}")


def show_main_menu():
    header("💰 Smart Expense Tracker")
    options = [
        ("1", "Add Expense"),
        ("2", "View All Expenses"),
        ("3", "View by Category"),
        ("4", "View by Month"),
        ("5", "Analytics & Summary"),
        ("6", "Edit Expense"),
        ("7", "Delete Expense"),
        ("0", "Exit"),
    ]
    for key, label in options:
        print(f"  [{key}]  {label}")
    print()