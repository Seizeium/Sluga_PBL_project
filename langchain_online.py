import os
import gspread
import pandas as pd
from langchain.tools import Tool
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetManager:
    def __init__(self, json_keyfile, sheet_name):
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, self.scope)
        self.client = gspread.authorize(self.creds)
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
        for i in range(1, len(df) + 2):  # +2 to include header
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


# === LangChain Tool Registration ===

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
                           description="Add/Update a column. Args: column_name:str, values_list:list")
    ]
    return tools
