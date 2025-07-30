import re
from datetime import datetime, timedelta
import pandas as pd

class FormatParserr:
    def __init__(self):
        pass

    def parse_amount(self, value, detected_format=None):
        """
        Parses complex amount formats: symbols, M/K, negatives in parentheses, etc.
        Examples: "$1,234.56", "(2,500.00)", "1.5M", "₹1,23,456"
        """
        value_str = str(value).strip().replace(",", "")
        multiplier = 1

        # Handle negative amounts in parentheses
        if value_str.startswith("(") and value_str.endswith(")"):
            multiplier = -1
            value_str = value_str[1:-1]

        # Remove any currency symbols or extra characters
        value_str = re.sub(r"[^\d.\-MKmk]", "", value_str)

        # Handle suffixes like M (million), K (thousand), B (billion)
        if value_str.endswith(('M', 'm')):
            multiplier *= 1_000_000
            value_str = value_str[:-1]
        elif value_str.endswith(('K', 'k')):
            multiplier *= 1_000
            value_str = value_str[:-1]
        elif value_str.endswith(('B', 'b')):
            multiplier *= 1_000_000_000
            value_str = value_str[:-1]

        try:
            return float(value_str) * multiplier
        except:
            return None

    def parse_date(self, value, detected_format=None):
        """
        Parses standard and special formats:
        - Standard dates: '2023-12-31', '12/31/2023'
        - Quarters: 'Q4 2023'
        - Short dates: 'Dec-23'
        - Excel serial: 44927 → date
        """
        if pd.isna(value):
            return None

        value_str = str(value).strip()

        # Excel serial number
        if re.fullmatch(r"\d{5}", value_str):
            try:
                return datetime(1899, 12, 30) + timedelta(days=int(value_str))
            except:
                pass

        # Quarter format: "Q4 2023"
        match = re.match(r"Q([1-4])\s*(\d{4})", value_str, re.IGNORECASE)
        if match:
            q, year = int(match.group(1)), int(match.group(2))
            month = 3 * q
            return datetime(year, month, 1)

        # Short month-year format: "Dec-23" or "Dec 23"
        try:
            return datetime.strptime(value_str, "%b-%y")
        except:
            pass

        # Use detected format if provided
        if detected_format:
            try:
                return datetime.strptime(value_str, detected_format)
            except:
                pass

        # Fallback to automatic parsing
        try:
            return pd.to_datetime(value_str, errors='coerce')
        except:
            return None

    def normalize_currency(self, value):
        """
        Converts common currency symbols to ISO codes.
        """
        symbol_map = {
            "$": "USD",
            "€": "EUR",
            "£": "GBP",
            "₹": "INR",
        }
        for symbol, code in symbol_map.items():
            if symbol in str(value):
                return code
        return "UNKNOWN"

    def handle_special_formats(self, value):
        """
        Handle percentages, negative parentheses, etc.
        """
        value_str = str(value).strip()

        # Handle percentages
        if value_str.endswith('%'):
            try:
                return float(value_str.strip('%')) / 100
            except:
                return None

        # Handle negative numbers in parentheses
        if value_str.startswith('(') and value_str.endswith(')'):
            try:
                return -float(re.sub(r'[^\d.]', '', value_str))
            except:
                return None

        return value
