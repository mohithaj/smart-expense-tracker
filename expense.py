"""
expense.py - Expense data model using OOP
"""
from datetime import datetime


class Expense:
    """Represents a single expense entry."""

    CATEGORIES = [
        "Food & Dining",
        "Transport",
        "Shopping",
        "Entertainment",
        "Health & Medical",
        "Bills & Utilities",
        "Education",
        "Travel",
        "Other",
    ]

    def __init__(self, amount: float, category: str, description: str,
                 date: str = None, expense_id: int = None):
        self.id = expense_id
        self.amount = round(float(amount), 2)
        self.category = category
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return (
            f"[ID: {self.id or 'N/A'}] {self.date} | "
            f"{self.category:<20} | ₹{self.amount:>8.2f} | {self.description}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @staticmethod
    def validate_amount(amount_str: str) -> float:
        """Validate and convert amount string to float."""
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
            return amount
        except ValueError:
            raise ValueError(f"Invalid amount: '{amount_str}'. Enter a positive number.")

    @staticmethod
    def validate_category(choice: str) -> str:
        """Validate category choice by index."""
        try:
            index = int(choice) - 1
            if 0 <= index < len(Expense.CATEGORIES):
                return Expense.CATEGORIES[index]
            raise ValueError
        except (ValueError, IndexError):
            raise ValueError(f"Invalid choice. Pick 1–{len(Expense.CATEGORIES)}.")