import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials



def authenticate_google_sheets(credentials_file=r"C:\Users\sonaw\PBL\credentials.json.json"):
    """Authenticate the Google Sheets API and return the client."""
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    return client

def read_google_sheet(sheet_url, sheet_name):
    """Read a Google Sheet into a pandas DataFrame."""
    client = authenticate_google_sheets()
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(sheet_name)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df

def update_google_sheet(sheet_url, sheet_name, row, col, value):
    """Update a cell in a Google Sheet."""
    client = authenticate_google_sheets()
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.worksheet(sheet_name)
    worksheet.update_cell(row, col, value)

def add_row(df, row_index, selected_columns=None):
    """Add specific cells of a particular row (specified by row_index) based on selected columns."""
    if 0 <= row_index < len(df):
        if selected_columns is None:
            return df.iloc[row_index].sum()
        total = 0
        for column in selected_columns:
            if column in df.columns:
                total += df.iloc[row_index][column]
            else:
                print(f"Invalid column name: {column}. Skipping this column.")
        return total
    else:
        print("Invalid row index.")
        return None

def add_column(df, column_name, selected_rows=None):
    """Add specific cells of a particular column (specified by column_name) based on selected rows."""
    if column_name in df.columns:
        if selected_rows is None:
            return df[column_name].sum()
        total = 0
        for row in selected_rows:
            if 0 <= row < len(df):
                total += df.iloc[row][column_name]
            else:
                print(f"Invalid row index: {row}. Skipping this row.")
        return total
    else:
        print("Invalid column name.")
        return None

def calculate_attendance(df, student_name):
    """Calculate the total attendance of a particular student based on the given student name."""
    if student_name in df['Student Name'].values:
        student_row = df[df['Student Name'] == student_name]
        attendance_columns = df.columns[1:]
        attendance = student_row[attendance_columns].apply(lambda x: x == 'P').sum(axis=1).values[0]
        return attendance
    else:
        print(f"Student '{student_name}' not found in the data.")
        return None

def calculate_defaulter(df, student_name, threshold=0.5):
    """Determine if a student is a defaulter based on attendance."""
    if student_name in df['Student Name'].values:
        student_row = df[df['Student Name'] == student_name]
        attendance_columns = df.columns[1:]
        total_days = len(attendance_columns)
        absences = student_row[attendance_columns].apply(lambda x: x == 'A').sum(axis=1).values[0]
        absence_rate = absences / total_days
        return absence_rate > threshold
    else:
        print(f"Student '{student_name}' not found in the data.")
        return None

def calculate_percentage(df, student_name):
    """Calculate the percentage of a student based on their marks."""
    if student_name in df['Student Name'].values:
        student_row = df[df['Student Name'] == student_name]
        score_columns = df.select_dtypes(include='number').columns
        total_marks = student_row[score_columns].sum(axis=1).values[0]
        max_marks = len(score_columns) * 100
        return (total_marks / max_marks) * 100
    else:
        print(f"Student '{student_name}' not found in the data.")
        return None

def main():
    # Ask user for the Google Sheet URL and the sheet name
    sheet_url = input("Enter the URL of the Google Sheet: ")
    sheet_name = input("Enter the name of the sheet (e.g., 'Sheet1'): ")

    # Read the Google Sheet
    df = read_google_sheet(sheet_url, sheet_name)
    if df is None:
        return

    print("\nData in the Google Sheet:")
    print(df)

    # Ask user for action: row, column, attendance, defaulter, percentage
    choice = input("\nDo you want to add values of a row, column, calculate attendance, check defaulter status, or calculate percentage? (Enter 'row', 'column', 'attendance', 'defaulter', or 'percentage'): ").strip().lower()

    if choice == 'row':
        row_index = int(input("Enter the row index to sum (starting from 0): "))
        selected_columns_input = input("Enter the column names to sum (comma-separated, or press Enter to sum the entire row): ").strip()
        if selected_columns_input:
            selected_columns = [x.strip() for x in selected_columns_input.split(',')]
        else:
            selected_columns = None
        result = add_row(df, row_index, selected_columns)
        if result is not None:
            print(f"Sum of the selected cells in row {row_index}: {result}")
    elif choice == 'column':
        column_name = input("Enter the column name to sum: ")
        selected_rows_input = input("Enter the row indices to sum (comma-separated, or press Enter to sum the entire column): ").strip()
        if selected_rows_input:
            selected_rows = [int(x.strip()) for x in selected_rows_input.split(',')]
        else:
            selected_rows = None
        result = add_column(df, column_name, selected_rows)
        if result is not None:
            print(f"Sum of the selected rows in column '{column_name}': {result}")
    elif choice == 'attendance':
        student_name = input("Enter the student's name to calculate their attendance: ")
        attendance = calculate_attendance(df, student_name)
        if attendance is not None:
            print(f"Total attendance for '{student_name}': {attendance}")
    elif choice == 'defaulter':
        student_name = input("Enter the student's name to check their defaulter status: ")
        defaulter = calculate_defaulter(df, student_name)
        if defaulter is not None:
            if defaulter:
                print(f"{student_name} is a defaulter.")
            else:
                print(f"{student_name} is not a defaulter.")
    elif choice == 'percentage':
        student_name = input("Enter the student's name to calculate their percentage: ")
        percentage = calculate_percentage(df, student_name)
        if percentage is not None:
            print(f"Percentage for '{student_name}': {percentage:.2f}%")
    else:
        print("Invalid choice. Please enter 'row', 'column', 'attendance', 'defaulter', or 'percentage'.")

if __name__ == "__main__":
    main()

