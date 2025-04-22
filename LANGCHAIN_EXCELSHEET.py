import os
import pandas as pd
from langchain.tools import Tool
from typing import List, Dict, Any

# ---------- Excel Sheet Manager Class ----------

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

# ---------- Excel Data Handling Functions ----------

def read_excel_file(file_path: str) -> pd.DataFrame:
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read Excel file: {e}")

def sum_row(file_path: str, row_index: int, selected_columns: List[str] = None) -> float:
    df = read_excel_file(file_path)
    if selected_columns:
        numeric_values = pd.to_numeric(df.loc[row_index, selected_columns], errors='coerce')
    else:
        numeric_values = pd.to_numeric(df.loc[row_index], errors='coerce')
    return numeric_values.sum()

def sum_column(file_path: str, column_name: str) -> float:
    df = read_excel_file(file_path)
    numeric_values = pd.to_numeric(df[column_name], errors='coerce')
    return numeric_values.sum()

def calculate_attendance(file_path: str, student_name: str, total_days_column: str, present_days_column: str) -> str:
    df = read_excel_file(file_path)
    student_row = df[df['Student Name'] == student_name]
    if student_row.empty:
        return f"Student {student_name} not found."

    total_days = student_row.iloc[0][total_days_column]
    present_days = student_row.iloc[0][present_days_column]

    try:
        percentage = (present_days / total_days) * 100
        return f"{student_name}'s attendance percentage is {percentage:.2f}%"
    except (ZeroDivisionError, TypeError):
        return "Invalid attendance data."

def calculate_percentage(file_path: str, subjects: List[str], max_marks: Dict[str, float]) -> str:
    df = read_excel_file(file_path)

    if not all(subj in max_marks for subj in subjects):
        return "Missing max marks for some subjects."

    result_df = pd.DataFrame()
    result_df['Student Name'] = df['Student Name']

    total_scores = [df[subj] for subj in subjects]
    total_scores_df = pd.concat(total_scores, axis=1)
    obtained_total = total_scores_df.sum(axis=1)
    max_total = sum(max_marks[subj] for subj in subjects)

    result_df['Percentage'] = (obtained_total / max_total) * 100

    return result_df.to_json(orient='records')

def calculate_defaulter(file_path: str, student_name: str, total_days_column: str, present_days_column: str, threshold: float = 75.0) -> str:
    df = read_excel_file(file_path)
    student_row = df[df['Student Name'] == student_name]
    if student_row.empty:
        return f"Student {student_name} not found."

    total_days = student_row.iloc[0][total_days_column]
    present_days = student_row.iloc[0][present_days_column]

    try:
        absence_rate = 100 - (present_days / total_days) * 100
        if absence_rate > (100 - threshold):
            return f"{student_name} is a defaulter."
        else:
            return f"{student_name} is not a defaulter."
    except (ZeroDivisionError, TypeError):
        return "Invalid attendance data."

# ---------- LangChain Tool Wrappers ----------

def sum_row_tool(file_path: str, row_index: int, selected_columns: List[str] = None) -> str:
    result = sum_row(file_path, row_index, selected_columns)
    return f"Sum of row {row_index}: {result}"

def sum_column_tool(file_path: str, column_name: str) -> str:
    result = sum_column(file_path, column_name)
    return f"Sum of column '{column_name}': {result}"

def calculate_attendance_tool(file_path: str, student_name: str, total_days_column: str, present_days_column: str) -> str:
    return calculate_attendance(file_path, student_name, total_days_column, present_days_column)

def calculate_percentage_tool(file_path: str, subjects: List[str], max_marks: Dict[str, float]) -> str:
    return calculate_percentage(file_path, subjects, max_marks)

def calculate_defaulter_tool(file_path: str, student_name: str, total_days_column: str, present_days_column: str, threshold: float = 75.0) -> str:
    return calculate_defaulter(file_path, student_name, total_days_column, present_days_column, threshold)

# ---------- LangChain Tool Registrations ----------

tools = [
    Tool.from_function(func=sum_row_tool, name="SumRow", description="Sum numeric values in a specified row from an Excel file, optionally for selected columns."),
    Tool.from_function(func=sum_column_tool, name="SumColumn", description="Sum numeric values in a specified column from an Excel file."),
    Tool.from_function(func=calculate_attendance_tool, name="CalculateAttendance", description="Calculate attendance percentage for a student from an Excel file."),
    Tool.from_function(func=calculate_percentage_tool, name="CalculatePercentage", description="Calculate percentage for each student based on selected subjects and maximum marks."),
    Tool.from_function(func=calculate_defaulter_tool, name="CalculateDefaulter", description="Determine if a student is a defaulter based on attendance percentage threshold.")
]
