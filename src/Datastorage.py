import pandas as pd

class DataStoragee:
    def __init__(self):
        self.data = []  # List of dicts: {"df": dataframe, "meta": metadata}

    def store_data(self, dataframe, metadata):
        self.data.append({"df": dataframe, "meta": metadata})
        print("✅ Data stored with metadata.")

    def create_indexes(self, columns):
        print(f"✅ Index request received for: {columns}")
        # No actual indexing for pandas in-memory, but printed for logging

    def query_by_criteria(self, filters):
        """
        filters: dictionary like {"Currency Code": "HUF"}
        """
        results = []

        for record in self.data:
            df = record["df"]
            filtered_df = df.copy()

            for col, value in filters.items():
                if col in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[col] == value]
                else:
                    print(f"⚠️ Filter column '{col}' not found in this sheet.")
                    filtered_df = pd.DataFrame()  # stop further filtering
                    break

            if not filtered_df.empty:
                results.append(filtered_df)

        return results

    def aggregate_data(self, group_by, measures):
        """
        group_by: list of column names
        measures: list of numeric columns to aggregate (sum)
        """
        aggregated_results = []

        for record in self.data:
            df = record["df"]
            missing = [col for col in group_by + measures if col not in df.columns]

            if missing:
                print(f"⚠️ Skipping aggregation due to missing columns: {missing}")
                continue

            grouped = df.groupby(group_by)[measures].sum().reset_index()
            aggregated_results.append(grouped)

        return aggregated_results
