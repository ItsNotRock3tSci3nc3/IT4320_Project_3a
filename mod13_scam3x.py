import unittest
from validator import (
    validate_symbol,
    validate_chart_type,
    validate_time_series,
    validate_date
)

class TestProject3Inputs(unittest.TestCase):

    # -------------------------
    # SYMBOL TESTS
    # -------------------------
    def test_symbol_valid(self):
        self.assertTrue(validate_symbol("AAPL"))
        self.assertTrue(validate_symbol("GOOG"))
        self.assertTrue(validate_symbol("T"))
        self.assertTrue(validate_symbol("MSFT"))

    def test_symbol_invalid(self):
        self.assertFalse(validate_symbol("aaPL"))    # lowercase
        self.assertFalse(validate_symbol("AAPL!"))   # special char
        self.assertFalse(validate_symbol("123"))     # digits
        self.assertFalse(validate_symbol("TOOLONG8")) # > 7 chars

    # -------------------------
    # CHART TYPE TESTS
    # -------------------------
    def test_chart_type_valid(self):
        self.assertTrue(validate_chart_type("1"))
        self.assertTrue(validate_chart_type("2"))

    def test_chart_type_invalid(self):
        self.assertFalse(validate_chart_type("0"))
        self.assertFalse(validate_chart_type("3"))
        self.assertFalse(validate_chart_type("line"))
        self.assertFalse(validate_chart_type(""))

    # -------------------------
    # TIME SERIES TESTS
    # -------------------------
    def test_time_series_valid(self):
        for s in ["1", "2", "3", "4"]:
            self.assertTrue(validate_time_series(s))

    def test_time_series_invalid(self):
        self.assertFalse(validate_time_series("0"))
        self.assertFalse(validate_time_series("5"))
        self.assertFalse(validate_time_series("open"))
        self.assertFalse(validate_time_series(""))

    # -------------------------
    # DATE TESTS
    # -------------------------
    def test_date_valid(self):
        self.assertTrue(validate_date("2024-01-01"))
        self.assertTrue(validate_date("1999-12-31"))

    def test_date_invalid(self):
        self.assertFalse(validate_date("01-01-2024"))
        self.assertFalse(validate_date("2024/01/01"))
        self.assertFalse(validate_date("2024-13-01"))
        self.assertFalse(validate_date("not-a-date"))
        self.assertFalse(validate_date(""))

if __name__ == "__main__":
    unittest.main()
