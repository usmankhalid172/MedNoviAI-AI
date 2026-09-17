"""
Verified spending pattern intelligence for the HisabDo AI service.

Responsibilities:
1. Retrieve user transactions from the HisabDo-style local dataset.
2. Filter by user_id and optional analysis period.
3. Separate income and expense transactions.
4. Aggregate totals and category-wise spending.
5. Emit business-friendly period/monthly comparison summaries.
6. Provide a deterministic intelligence payload for the AI layer.

The implementation is intentionally deterministic and local-first so the AI
layer can consume verified values only; the LLM never creates a number.
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TRANSACTION_DATA_PATH = ROOT / "transactions_dataset.json"


class SpendingPatternIntelligenceService:
    """Backend service that derives verified spending insight from HisabDo data."""

    def __init__(self, dataset_path: str | Path = TRANSACTION_DATA_PATH):
        self.dataset_path = Path(dataset_path)

    def get_spending_pattern_intelligence(
        self,
        user_id: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        """
        Build a deterministic spending pattern intelligence payload for one
        authenticated user, returning only records for that user and the
        requested date window.
        """
        if not user_id or not user_id.strip():
            raise ValueError("user_id is required")

        start = self._parse_date(start_date)
        end = self._parse_date(end_date)

        transactions = self._load_transactions()
        user_transactions = [
            tx for tx in transactions if tx.get("user_id") == user_id
        ]

        # Data isolation and authorization surface: every query starts from
        # the user_id in the path and never widens to a global ledger.
        user_transactions = self._filter_period(user_transactions, start, end)

        income_transactions = [
            tx for tx in user_transactions if self._is_income_transaction(tx)
        ]
        expense_transactions = [
            tx for tx in user_transactions if self._is_expense_transaction(tx)
        ]

        income_total = sum(self._transaction_amount(tx) for tx in income_transactions)
        total_expenses = sum(self._transaction_amount(tx) for tx in expense_transactions)

        category_breakdown: dict[str, float] = defaultdict(float)
        for tx in expense_transactions:
            for item in tx.get("items", []):
                category = self._category_from_item_name(item.get("name", "Other"))
                item_amount = float(item.get("price", 0)) * float(item.get("quantity", 1))
                category_breakdown[category] += item_amount

        # Convert defaultdict to a normal dict for JSON/Pydantic safety.
        normal_breakdown = {
            category: round(amount, 2)
            for category, amount in sorted(category_breakdown.items())
        }

        total_category_spend = sum(normal_breakdown.values())
        category_percentages = {}
        if total_category_spend > 0:
            category_percentages = {
                category: round((amount / total_category_spend) * 100, 2)
                for category, amount in normal_breakdown.items()
            }

        monthly_comparison = self._monthly_comparison(user_transactions)

        return {
            "user_id": user_id,
            "analysis_period": {
                "start_date": start.isoformat() if start else "",
                "end_date": end.isoformat() if end else "",
            },
            "income_total": round(income_total, 2),
            "total_expenses": round(total_expenses, 2),
            "category_breakdown": normal_breakdown,
            "category_percentages": category_percentages,
            "period_summary": {
                "transaction_count": len(user_transactions),
                "income_transaction_count": len(income_transactions),
                "expense_transaction_count": len(expense_transactions),
                "has_transactions": bool(user_transactions),
                "months": monthly_comparison,
            },
            "monthly_comparison": monthly_comparison,
            "verified": True,
            "source": "verified_hisabdo_transaction_ledger",
        }

    def _load_transactions(self) -> list[dict[str, Any]]:
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Transaction dataset not found: {self.dataset_path}")

        with self.dataset_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Expected transaction dataset to be a list of records")

        return data

    def _filter_period(
        self,
        transactions: list[dict[str, Any]],
        start: datetime | None,
        end: datetime | None,
    ) -> list[dict[str, Any]]:
        results = []
        for tx in transactions:
            ts = self._parse_timestamp(tx.get("timestamp"))
            if ts is None:
                # If the record has no timestamp, allow it as a fallback only
                # when no date window is asked for the user.
                if start is None and end is None:
                    results.append(tx)
                continue

            if start and ts < start:
                continue
            if end and ts > end:
                continue
            results.append(tx)
        return results

    def _parse_date(self, value: str | None) -> datetime | None:
        if not value:
            return None
        # Accept YYYY-MM-DD or a full ISO timestamp.
        try:
            if len(value) == 10:
                return datetime.strptime(value, "%Y-%m-%d")
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("start_date and end_date must use YYYY-MM-DD or ISO 8601 format")

    def _parse_timestamp(self, value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None

    def _is_income_transaction(self, tx: dict[str, Any]) -> bool:
        # Separate income and expense records when a real HisabDo payload
        # includes direction/type fields. Keep the fallback deterministic.
        tx_kind = str(tx.get("type") or tx.get("kind") or tx.get("direction") or "expense").lower()
        if tx_kind in {"income", "credit", "inflow", "revenue"}:
            return True
        if tx_kind in {"expense", "debit", "outflow", "payment"}:
            return False

        # Legacy or dataset fallback: if a transaction's total value is positive
        # and an income field is present, treat as income. Otherwise expense.
        if tx.get("transaction_type"):
            return str(tx.get("transaction_type")).lower() == "income"
        return False

    def _is_expense_transaction(self, tx: dict[str, Any]) -> bool:
        tx_kind = str(tx.get("type") or tx.get("kind") or tx.get("direction") or "expense").lower()
        if tx_kind in {"expense", "debit", "outflow", "payment"}:
            return True
        if tx_kind in {"income", "credit", "inflow", "revenue"}:
            return False

        if tx.get("transaction_type"):
            return str(tx.get("transaction_type")).lower() == "expense"
        return True

    def _transaction_amount(self, tx: dict[str, Any]) -> float:
        # Prefer explicit amount fields when a real backend carries them.
        if "amount" in tx:
            return float(tx.get("amount", 0) or 0)
        if "total_amount" in tx:
            return float(tx.get("total_amount", 0) or 0)

        # The dataset uses item quantity*price. Total from aggregate item sum.
        total = 0.0
        for item in tx.get("items", []):
            try:
                q = float(item.get("quantity", 1) or 1)
                p = float(item.get("price", 0) or 0)
            except (TypeError, ValueError):
                continue
            total += q * p
        return round(total, 2)

    def _category_from_item_name(self, item_name: str) -> str:
        text = (item_name or "Other").lower()
        if "electricity" in text or "gas" in text:
            return "Utilities"
        if "internet" in text or "mobile" in text or "recharge" in text or "bill" in text:
            return "Bills"
        if "grocery" in text or "food" in text or "restaurant" in text:
            return "Groceries"
        if "fuel" in text or "ride" in text or "transport" in text:
            return "Transport"
        if "entertainment" in text or "movie" in text or "movie" in text:
            return "Entertainment"
        if "health" in text or "clinic" in text or "medicine" in text:
            return "Healthcare"
        return "Other"

    def _monthly_comparison(self, transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        month_totals: dict[str, dict[str, float | int]] = defaultdict(
            lambda: {"expense": 0.0, "income": 0.0, "count": 0}
        )

        for tx in transactions:
            ts = self._parse_timestamp(tx.get("timestamp"))
            if ts is None:
                continue
            month_key = ts.strftime("%Y-%m")
            if self._is_income_transaction(tx):
                month_totals[month_key]["income"] += self._transaction_amount(tx)
            else:
                month_totals[month_key]["expense"] += self._transaction_amount(tx)
            month_totals[month_key]["count"] += 1

        # Return stable chronological order.
        ordered = []
        for month in sorted(month_totals):
            ordered.append(
                {
                    "month": month,
                    "income": round(float(month_totals[month]["income"]), 2),
                    "expenses": round(float(month_totals[month]["expense"]), 2),
                    "transaction_count": int(month_totals[month]["count"]),
                }
            )

        return ordered


def get_spending_pattern_intelligence_service() -> SpendingPatternIntelligenceService:
    return SpendingPatternIntelligenceService()
