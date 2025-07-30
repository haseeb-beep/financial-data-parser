import pandas as pd
import numpy as np
import openpyxl
import sqlite3
import re
import re
from datetime import datetime
from decimal import Decimal
import locale


class Excelprocessor:
    def __init__(self):
        self.file={}

    def loadfile(self,filepaths):
        for path in filepaths:
            try:
                data=pd.read_excel(path,sheet_name=None,engine='openpyxl')
                self.file[path]=data
                print(f"Loaded {path} with {len(data)} sheet(s).")

            except Exception as e:
                print(f"Error Loading {path}: {e}")

    def getsheetinfo(self):
        for file_path, sheets in self.file.items():
            print(f"\n File: {file_path}")
            for sheet_name, df in sheets.items():
                print(f"  └─ Sheet: {sheet_name}, Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    def extractdata(self,sheet_name):
        extracted={}
        for file_paths,sheets in self.file.items():
            if sheet_name in sheets:
                extracted[file_paths]=sheets[sheet_name]

            else:
                print(f"file name not found in : {file_paths}")
        return extracted

    def preview_data(self, rows=5):
        """Preview first few rows of each sheet in each file"""
        for file_path, sheets in self.file.items():
            print(f"\n📦 File: {file_path}")
            for sheet_name, df in sheets.items():
                print(f"\n--- Sheet: {sheet_name} ---")
                print(df.head(rows))
                print(f"[{df.shape[0]} rows x {df.shape[1]} columns]")
                print("-" * 80)


