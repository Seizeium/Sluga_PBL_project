import os
import gspread
import pandas as pd
from langchain.tools import Tool
from oauth2client.service_account import ServiceAccountCredentials

# ---------------- Google Sheets Authentication ----------------

def authenticate_google_sheets(credentials_file=r"C:\Users\sonaw\PBL\credentials.json.json"):
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    return client

# ---------------- GoogleSheetManager Class ----------------

class GoogleSheetManager:
    def __init__(self, json_keyfile, sheet_name):
        self.client = authenticate_google_sheets(json_keyfile)
        self.sheet = self.client.open(sheet_name).sheet1
        self.headers = self.sheet.row_values(1) if self.sheet.row_values(1) else []

    def create_sheet(self, file_name: str, email: str, headers: list):
        new_file = self.client.create(file_name)
        new_file.share(email, perm_type='user', role='writer')
        self.sheet = new_file.sheet1
        self.sheet.append_row(headers)
        self.headers = headers
        return f"Sheet '{file_name}' created with headers: {headers}"

    def enter_data(self, rows: list):
        if not self.headers:
            raise ValueError("Headers not set. Please create the sheet with headers first.")
        for row_data in rows:
            if len(row_data) != len(self.headers):
                raise ValueError(f"Row length {len(row_data)} doesn't match header length {len(self.headers)}.")
            self.sheet.append_row(row_data)
        return f"{len(rows)} rows added successfully."

    def display_sheet(self):
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        return df.to_string(index=False)

    def edit_cell(self, row_num: int, column_name: str, new_value: str):
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        if column_name not in df.columns:
            raise ValueError("Invalid column name.")
        self.sheet.update_cell(row_num + 1, df.columns.get_loc(column_name) + 1, new_value)
        return f"Cell at row {row_num}, column '{column_name}' updated to '{new_value}'."

    def delete_row(self, row_num: int):
        self.sheet.delete_rows(row_num)
        return f"Row {row_num} deleted."

    def delete_column(self, column_name: str):
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        if column_name not in df.columns:
            return f"Column '{column_name}' does not exist."
        col_index = df.columns.get_loc(column_name) + 1
        for i in range(1, len(df) + 2):
            self.sheet.update_cell(i, col_index, "")
        return f"Column '{column_name}' deleted."

    def add_to_specific_row(self, row_num: int, column_name: str, new_value: str):
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        if column_name not in df.columns:
            raise ValueError("Invalid column name.")
        self.sheet.update_cell(row_num, df.columns.get_loc(column_name) + 1, new_value)
        return f"Updated row {row_num}, column '{column_name}' with '{new_value}'."

    def add_to_specific_column(self, column_name: str, values_list: list):
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        if column_name not in df.columns:
            df[column_name] = ""
        for i, value in enumerate(values_list, start=2):
            self.sheet.update_cell(i, df.columns.get_loc(column_name) + 1, value)
        return f"Column '{column_name}' updated."

# ---------------- Google Sheets Operations (Direct) ----------------

def read_google_sheet(sheet_url, sheet_name):
    client = authenticate_google_sheets()
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(sheet_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def update_google_sheet(sheet_url, sheet_name, row, col, value):
    client = authenticate_google_sheets()
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(sheet_name)
    worksheet.update_cell(row, col, value)

# ---------------- Data Analysis Functions ----------------

def add_row(df, row_index, selected_columns=None):
    if 0 <= row_index < len(df):
        if selected_columns is None:
            return df.iloc[row_index].sum()
        total = sum(df.iloc[row_index][col] for col in selected_columns if col in df.columns)
        return total
    else:
        return "Invalid row index."

def add_column(df, column_name, selected_rows=None):
    if column_name in df.columns:
        if selected_rows is None:
            return df[column_name].sum()
        total = sum(df.iloc[row][column_name] for row in selected_rows if 0 <= row < len(df))
        return total
    else:
        return f"Invalid column name: {column_name}"

def calculate_attendance(df, student_name):
    if student_name in df['Student Name'].values:
        student_row = df[df['Student Name'] == student_name]
        attendance_columns = df.columns[1:]
        attendance = student_row[attendance_columns].apply(lambda x: x == 'P').sum(axis=1).values[0]
        return int(attendance)
    else:
        return f"Student '{student_name}' not found."

def calculate_defaulter(df, student_name, threshold=0.5):
    if student_name in df['Student Name'].values:
        student_row = df[df['Student Name'] == student_name]
        attendance_columns = df.columns[1:]
        total_days = len(attendance_columns)
        absences = student_row[attendance_columns].apply(lambda x: x == 'A').sum(axis=1).values[0]
        absence_rate = absences / total_days
        return absence_rate > threshold
    else:
        return f"Student '{student_name}' not found."

def calculate_percentage(df, max_marks_per_subject, score_columns):
    valid_columns = [col for col in score_columns if col in df.columns]
    if not valid_columns:
        return "No valid columns provided."
    df['TOTAL'] = df[valid_columns].sum(axis=1)
    max_total_marks = len(valid_columns) * max_marks_per_subject
    df['percentage'] = (df['TOTAL'] / max_total_marks) * 100
    return df[['Student Name', 'TOTAL', 'percentage']].to_dict(orient='records')

# ---------------- LangChain Tool Registration ----------------

def get_google_sheet_tools(json_keyfile, sheet_name):
    manager = GoogleSheetManager(json_keyfile, sheet_name)
    tools = [
        Tool.from_function(func=manager.create_sheet, name="CreateSheet",
                           description="Create a new sheet with headers. Args: file_name:str, email:str, headers:list"),
        Tool.from_function(func=manager.enter_data, name="EnterData",
                           description="Enter rows of data into the sheet. Args: rows:list"),
        Tool.from_function(func=manager.display_sheet, name="DisplaySheet",
                           description="Display the sheet content as a table."),
        Tool.from_function(func=manager.edit_cell, name="EditCell",
                           description="Edit a specific cell. Args: row_num:int, column_name:str, new_value:str"),
        Tool.from_function(func=manager.delete_row, name="DeleteRow",
                           description="Delete a row by its number. Args: row_num:int"),
        Tool.from_function(func=manager.delete_column, name="DeleteColumn",
                           description="Delete a column by name. Args: column_name:str"),
        Tool.from_function(func=manager.add_to_specific_row, name="AddToSpecificRow",
                           description="Add data to a specific row. Args: row_num:int, column_name:str, new_value:str"),
        Tool.from_function(func=manager.add_to_specific_column, name="AddToSpecificColumn",
                           description="Add/Update a column. Args: column_name:str, values_list:list"),
        Tool.from_function(func=lambda sheet_url, sname: read_google_sheet(sheet_url, sname).to_dict(orient='records'),
                           name="ReadGoogleSheet",
                           description="Reads a Google Sheet and returns its content as a list of records."),
        Tool.from_function(func=update_google_sheet,
                           name="UpdateGoogleSheetCell",
                           description="Updates a specific cell in a Google Sheet."),
    ]
    return tools
