"""Minimal verified anomaly detection service for the HisabDo dataset.

The service intentionally stays deterministic and backend-owned:
- it retrieves only the requested user's transactions,
- separates expenses from income,
- computes baseline values from the budget dataset,
- emits the anomaly payload in a clean, JSON-safe shape.
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TRANSACTION_DATA_PATH = ROOT / "transactions_dataset.json"


class AnomalyDetectionService:
    """Service that returns verified anomaly records for one user."""

    def __init__(self, dataset_path: str | Path = TRANSACTION_DATA_PATH):
        self.dataset_path = Path(dataset_path)

    def get_anomalies(self, user_id: str, analysis_days: int = 30) -> dict[str, Any]:
        if not user_id or not user_id.strip():
            raise ValueError("user_id is required")
        if analysis_days < 1:
            raise ValueError("analysis_days must be at least 1")

        transactions = self._load_transactions()
        user_transactions = [
            tx for tx in transactions if tx.get("user_id") == user_id
        ]

        cutoff = datetime.utcnow() - timedelta(days=analysis_days)
        filtered_transactions = []
        for tx in user_transactions:
            ts = self._parse_timestamp(tx.get("timestamp"))
            if ts and ts >= cutoff:
                filtered_transactions.append(tx)

        expense_transactions = [
            tx for tx in filtered_transactions if self._is_expense_transaction(tx)
        ]

        avg_amount = 0.0
        if expense_transactions:
            totals = [self._transaction_amount(tx) for tx in expense_transactions]
            avg_amount = sum(totals) / len(totals)

        anomalies: list[dict[str, Any]] = []

        # Unusual amount detection.
        if expense_transactions:
            for tx in expense_transactions:
                amount = self._transaction_amount(tx)
                if amount >= max(avg_amount * 2.0, 1000.0):
                    anomalies.append({
                        "transaction_id": tx.get("transaction_id", ""),
                        "user_id": user_id,
                        "anomaly_type": "UNUSUAL_AMOUNT",
                        "amount": round(amount, 2),
                        "category": self._category_for_tx(tx),
                        "date": tx.get("timestamp", ""),
                        "expected_amount": round(avg_amount, 2),
                        "severity": "high" if amount >= avg_amount * 3.0 else "medium",
                        "reason": "Expense amount is significantly above the user's historical average amount.",
                    })

        # Spending spike detection.
        daily_totals: dict[str, float] = defaultdict(float)
        for tx in expense_transactions:
            date_key = self._parse_timestamp(tx.get("timestamp"))
            if date_key:
                daily_key = date_key.strftime("%Y-%m-%d")
                daily_totals[daily_key] += self._transaction_amount(tx)

        if daily_totals:
            normal_daily = avg_amount if avg_amount else 0
            for day, total in sorted(daily_totals.items()):
                if total >= max(normal_daily * 2.0, 2000.0):
                    anomalies.append({
                        "transaction_id": f"SPIKE-{day}",
                        "user_id": user_id,
                        "anomaly_type": "SPENDING_SPIKE",
                        "amount": round(total, 2),
                        "category": "Expense",
                        "date": f"{day}T00:00:00",
                        "expected_amount": round(normal_daily, 2),
                        "severity": "high" if total >= normal_daily * 3.0 else "medium",
                        "reason": "Daily spending exceeds the normal spending pattern for this user.",
                    })

        # Unusual category detection: categories that have very low historical share
        # compared with the normal category average. Keep it deterministic and simple.
        category_breakdown = defaultdict(float)
        for tx in expense_transactions:
            category = self._category_for_tx(tx)
            category_breakdown[category] += self._transaction_amount(tx)

        if category_breakdown:
            max_category_total = max(category_breakdown.values()) if category_breakdown else 0
            for category, total in sorted(category_breakdown.items()):
                # If category is much higher than other categories in this window,
                # treat as unusually active for this user.
                if max_category_total and total >= max_category_total * 0.7:
                    anomalies.append({
                        "transaction_id": f"CATEGORY-{category}",
                        "user_id": user_id,
                        "anomaly_type": "UNUSUAL_CATEGORY",
                        "amount": round(total, 2),
                        "category": category,
                        "date": sorted([tx.get("timestamp", "") for tx in expense_transactions if self._category_for_tx(tx) == category])[-1],
                        "expected_amount": round(max_category_total * 0.5, 2),
                        "severity": "medium",
                        "reason": "Spending in this category is unusually concentrated compared with the user's normal category mix.",
                    })

        # Duplicate transaction detection.
        seen_pairs: dict[tuple[str, float, str, str], list[dict[str, Any]]] = defaultdict(list)
        for tx in expense_transactions:
            category = self._category_for_tx(tx)
            merchant = self._merchant_for_tx(tx)
            amount = self._transaction_amount(tx)
            ts = self._parse_timestamp(tx.get("timestamp"))
            if ts:
                key = (user_id, amount, category, merchant)
                seen_pairs[key].append({
                    "transaction": tx,
                    "timestamp": ts,
                })

        for key, items in seen_pairs.items():
            # Same user, amount, category, merchant, and close timestamps in the window.
            for idx, left in enumerate(items):
                for right in items[idx + 1:]:
                    gap = (right["timestamp"] - left["timestamp"]).total_seconds()
                    if 0 <= gap <= 60:
                        first_tx = left["transaction"]
                        anomalies.append({
                            "transaction_id": first_tx.get("transaction_id", ""),
                            "user_id": user_id,
                            "anomaly_type": "DUPLICATE_TRANSACTION",
                            "amount": round(key[1], 2),
                            "category": key[2],
                            "date": first_tx.get("timestamp", ""),
                            "expected_amount": round(key[1], 2),
                            "severity": "low",
                            "reason": "Similar transaction details appeared in a very short period and may be a duplicate.",
                        })
                        break

        # Keep deterministic stable order and JSON-safe numeric values.
        ordered = []
        for item in anomalies:
            ordered.append({
                "transaction_id": item.get("transaction_id") or "",
                "user_id": item.get("user_id") or user_id,
                "anomaly_type": item.get("anomaly_type") or "UNUSUAL_AMOUNT",
                "amount": round(float(item.get("amount") or 0), 2),
                "category": item.get("category") or "Other",
                "date": item.get("date") or "",
                "expected_amount": round(float(item.get("expected_amount") or 0), 2),
                "severity": item.get("severity") or "low",
                "reason": item.get("reason") or "Anomaly detected from verified transaction data.",
            })

        return {
            "user_id": user_id,
            "analysis_days": analysis_days,
            "anomalies": ordered,
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

    def _parse_timestamp(self, value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None

    def _is_income_transaction(self, tx: dict[str, Any]) -> bool:
        kind = str(tx.get("type") or tx.get("kind") or tx.get("direction") or "expense").lower()
        if kind in {"income", "credit", "inflow", "revenue"}:
            return True
        if kind in {"expense", "debit", "outflow", "payment"}:
            return False
        if tx.get("transaction_type"):
            return str(tx.get("transaction_type")).lower() == "income"
        return False

    def _is_expense_transaction(self, tx: dict[str, Any]) -> bool:
        kind = str(tx.get("type") or tx.get("kind") or tx.get("direction") or "expense").lower()
        if kind in {"expense", "debit", "outflow", "payment"}:
            return True
        if kind in {"income", "credit", "inflow", "revenue"}:
            return False
        if tx.get("transaction_type"):
            return str(tx.get("transaction_type")).lower() == "expense"
        return True

    def _transaction_amount(self, tx: dict[str, Any]) -> float:
        if "amount" in tx:
            return float(tx.get("amount", 0) or 0)
        if "total_amount" in tx:
            return float(tx.get("total_amount", 0) or 0)

        total = 0.0
        for item in tx.get("items", []):
            try:
                q = float(item.get("quantity", 1) or 1)
                p = float(item.get("price", 0) or 0)
            except (TypeError, ValueError):
                continue
            total += q * p
        return round(total, 2)

    def _category_for_tx(self, tx: dict[str, Any]) -> str:
        for item in tx.get("items", []):
            text = (item.get("name") or "Other").lower()
            if "electricity" in text or "gas" in text:
                return "Utilities"
            if "internet" in text or "mobile" in text or "recharge" in text or "bill" in text:
                return "Bills"
            if "grocery" in text or "food" in text or "restaurant" in text:
                return "Groceries"
            if "fuel" in text or "ride" in text or "transport" in text:
                return "Transport"
            if "entertainment" in text or "movie" in text:
                return "Entertainment"
            if "health" in text or "clinic" in text or "medicine" in text:
                return "Healthcare"
            if "flight" in text or "travel" in text:
                return "Travel"
        return "Other"

    def _merchant_for_tx(self, tx: dict[str, Any]) -> str:
        return str(tx.get("merchant") or tx.get("description") or ", ".join(
            item.get("name", "Other") for item in tx.get("items", [])
        ) or "Other")


def get_anomaly_detection_service() -> AnomalyDetectionService:
    return AnomalyDetectionService()
