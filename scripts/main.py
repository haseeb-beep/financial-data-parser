from src.Excelprocesssor import Excelprocessor
from src.datatype_detector import DataTypeDetector
from src.FormatParser import FormatParserr
from src.Datastorage import DataStoragee

# Step 1: Load Excel files
file_paths = [
    "../data/sample/Customer_Ledger_Entries_FULL.xlsx",
    "../data/sample/KH_Bank.xlsx"
]
processor = Excelprocessor()
processor.loadfile(file_paths)
processor.getsheetinfo()

detector = DataTypeDetector()
parser = FormatParserr()
storage = DataStoragee()

# Step 2: Loop through all sheets from all files
for file_path, sheets in processor.file.items():
    for sheet_name, df in sheets.items():
        print(f"\n📊 File: {file_path} → Sheet: {sheet_name}")
        print("────────────────────────────────────────────────────────────")

        parsed_df = df.copy()
        metadata = {}

        for col in df.columns:
            sample_values = df[col].dropna().astype(str).tolist()
            sample_preview = sample_values[:5]

            detected_type = detector.detececolumntype(sample_values)
            metadata[col] = detected_type

            print(f"\n🧠 Column: {col}")
            print(f"🔍 Detected Type: {detected_type}")

            parsed_values = []
            for raw_val in sample_preview:
                if detected_type == "Number":
                    parsed_val = parser.parse_amount(raw_val)
                elif detected_type == "Date":
                    parsed_val = parser.parse_date(raw_val)
                else:
                    parsed_val = raw_val
                parsed_values.append((raw_val, parsed_val))

            for raw, parsed in parsed_values:
                print(f"  Raw: {raw} → Parsed: {parsed}")

        # Step 3: Store cleaned data with metadata
        storage.store_data(parsed_df, metadata)

# Step 4: Indexing (for log only)
print("\n📁 Indexing 'Customer Name' and 'Currency Code'...")
storage.create_indexes(["Customer Name", "Currency Code"])

# Step 5: Query sample
print("\n🔎 Querying where Currency Code is 'HUF'...")
results = storage.query_by_criteria({"Currency Code": "HUF"})

if results:
    for i, df in enumerate(results):
        print(f"\n🔹 Result #{i + 1} (Rows: {len(df)})")
        print(df.head())
else:
    print("❌ No data matched the filter.")

# Step 6: Aggregation
print("\n📊 Aggregating 'Amount (LCY)' by 'Currency Code'...")
aggregated = storage.aggregate_data(group_by=["Currency Code"], measures=["Amount (LCY)"])

if aggregated:
    for i, agg_df in enumerate(aggregated):
        print(f"\n🔸 Aggregated Result #{i + 1}")
        print(agg_df.head())
else:
    print("❌ No valid aggregation found.")
