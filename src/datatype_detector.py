import pandas as pd
class DataTypeDetector:
    def __init__(self):
        pass

    def detececolumntype(self, series):
        series = pd.Series(series).dropna().astype(str)

        if series.empty:
            return "Unknown"
        elif self.is_date(series):
            return "Date"
        elif self.is_number(series):
            return "Number"
        else:
            return "String"

    def is_number(self, series):
        try:
            pd.to_numeric(series)
            return True
        except:
            return False

    def is_date(self, series):
        count = 0
        sample = series[:10]
        for val in sample:
            try:
                pd.to_datetime(val, errors='raise')
                count += 1
            except:
                continue
        return count >= len(sample) * 0.7
