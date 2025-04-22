import os
import pandas as pd

class ExcelSheetManager:
    def __init__(self):
        self.df = None

    def create_sheet(self, num_rows: int):
        self.df = pd.DataFrame(index=range(num_rows))
        print(f"[INFO] Created a new sheet with {num_rows} rows.")

    def enter_data(self, rows: list):
        if self.df is None:
            raise ValueError("No sheet initialized.")
        self.df = pd.DataFrame(rows)
        print("[INFO] Data entered into sheet.")

    def save_to_excel(self, filename: str):
        if self.df is None:
            raise ValueError("No sheet to save.")
        full_path = os.path.join(os.getcwd(), filename)
        self.df.to_excel(full_path, index=False)
        print(f"[INFO] Sheet saved to: {full_path}")

    def load_sheet(self, filename: str):
        full_path = os.path.join(os.getcwd(), filename)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File '{full_path}' not found.")
        self.df = pd.read_excel(full_path)
        print(f"[INFO] Loaded sheet from: {full_path}")

    def edit_cell(self, row: int, column: str, value):
        if self.df is None:
            raise ValueError("No sheet loaded.")
        self.df.at[row, column] = value
        print(f"[INFO] Edited cell at row {row}, column '{column}' to '{value}'.")

    def delete_row(self, row: int):
        if self.df is None:
            raise ValueError("No sheet loaded.")
        self.df = self.df.drop(index=row).reset_index(drop=True)
        print(f"[INFO] Deleted row {row}.")

    def delete_column(self, column: str):
        if self.df is None:
            raise ValueError("No sheet loaded.")
        self.df = self.df.drop(columns=[column])
        print(f"[INFO] Deleted column '{column}'.")
