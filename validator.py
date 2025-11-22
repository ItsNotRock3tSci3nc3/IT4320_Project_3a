# validators.py
import re
from datetime import datetime

def validate_symbol(symbol):
    """Symbol must be capital letters, length 1–7."""
    return bool(re.fullmatch(r"[A-Z]{1,7}", symbol))

def validate_chart_type(chart_type):
    """Chart type must be “1” or “2”."""
    return chart_type in ["1", "2"]

def validate_time_series(series):
    """Time series must be 1–4."""
    return series in ["1", "2", "3", "4"]

def validate_date(date_str):
    """Date must be YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False
