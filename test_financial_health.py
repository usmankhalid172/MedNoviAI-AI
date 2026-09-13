import unittest

from financial_health_scoring import FinancialData, calculate_financial_health_score


class FinancialHealthScoringTest(unittest.TestCase):
    def test_calculate_financial_health_score_returns_requested_payload_fields(self):
        data = FinancialData(
            total_income=150000,
            total_expense=108500,
            budget=103000,
            previous_expense=92000,
            debt_amount=12000,
            has_transactions=True,
        )

        result = calculate_financial_health_score(data)

        self.assertEqual(result["income"], 150000)
        self.assertEqual(result["expenses"], 108500)
        self.assertIn("budgetUtilization", result)
        self.assertIn("cashFlow", result)
        self.assertIn("factorScores", result)
        self.assertIn("savingBehavior", result["factorScores"])
        self.assertIn("expenseControl", result["factorScores"])
        self.assertIn("budgetControl", result["factorScores"])
        self.assertIn("cashFlow", result["factorScores"])
        self.assertIn("debtUdhaar", result["factorScores"])
        self.assertIn("expenseGrowth", result["factorScores"])


if __name__ == "__main__":
    unittest.main()
