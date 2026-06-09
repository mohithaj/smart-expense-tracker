"""
expense_manager.py - Core CRUD and analytics logic
"""
from database import get_connection
from expense import Expense
from datetime import datetime


class ExpenseManager:
    """Handles all database operations for expenses."""

    # ──────────────────────────────────────────
    # CREATE
    # ──────────────────────────────────────────

    def add_expense(self, expense: Expense) -> int:
        """Insert a new expense and return its ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
            (expense.amount, expense.category, expense.description, expense.date),
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    # ──────────────────────────────────────────
    # READ
    # ──────────────────────────────────────────

    def get_all_expenses(self) -> list[Expense]:
        """Return all expenses ordered by date descending."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC, id DESC")
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_expense(r) for r in rows]

    def get_expenses_by_category(self, category: str) -> list[Expense]:
        """Return expenses filtered by category."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM expenses WHERE category = ? ORDER BY date DESC",
            (category,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_expense(r) for r in rows]

    def get_expenses_by_month(self, year: int, month: int) -> list[Expense]:
        """Return expenses for a given year-month."""
        month_str = f"{year}-{month:02d}"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC",
            (f"{month_str}%",),
        )
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_expense(r) for r in rows]

    def get_expense_by_id(self, expense_id: int) -> Expense | None:
        """Return a single expense by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_expense(row) if row else None

    # ──────────────────────────────────────────
    # UPDATE
    # ──────────────────────────────────────────

    def update_expense(self, expense: Expense) -> bool:
        """Update an existing expense. Returns True if a row was changed."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE expenses
               SET amount=?, category=?, description=?, date=?
               WHERE id=?""",
            (expense.amount, expense.category, expense.description,
             expense.date, expense.id),
        )
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        return changed

    # ──────────────────────────────────────────
    # DELETE
    # ──────────────────────────────────────────

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense by ID. Returns True if deleted."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted

    # ──────────────────────────────────────────
    # ANALYTICS
    # ──────────────────────────────────────────

    def get_total(self, expenses: list[Expense]) -> float:
        return round(sum(e.amount for e in expenses), 2)

    def get_summary_by_category(self, expenses: list[Expense]) -> dict[str, float]:
        """Return {category: total_amount} sorted by total descending."""
        summary: dict[str, float] = {}
        for e in expenses:
            summary[e.category] = round(summary.get(e.category, 0) + e.amount, 2)
        return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))

    def get_monthly_summary(self) -> dict[str, float]:
        """Return {YYYY-MM: total} for all months in the DB."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total "
            "FROM expenses GROUP BY month ORDER BY month DESC"
        )
        rows = cursor.fetchall()
        conn.close()
        return {r["month"]: round(r["total"], 2) for r in rows}

    def get_highest_expense(self, expenses: list[Expense]) -> Expense | None:
        return max(expenses, key=lambda e: e.amount) if expenses else None

    def get_average_expense(self, expenses: list[Expense]) -> float:
        return round(sum(e.amount for e in expenses) / len(expenses), 2) if expenses else 0.0

    # ──────────────────────────────────────────
    # HELPER
    # ──────────────────────────────────────────

    @staticmethod
    def _row_to_expense(row) -> Expense:
        return Expense(
            amount=row["amount"],
            category=row["category"],
            description=row["description"],
            date=row["date"],
            expense_id=row["id"],
        )