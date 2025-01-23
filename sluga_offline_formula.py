import pandas as pd

def read_excel_file(file_path):
    """Read the Excel file and return the DataFrame."""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None

def add_row(df, row_index, selected_columns=None):
    """Add specific cells of a particular row (specified by row_index) based on selected columns."""
    if 0 <= row_index < len(df):
        # If no specific columns are selected, sum the entire row
        if selected_columns is None:
            return df.iloc[row_index].sum()
        
        # Sum only the values from the specified columns
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
        # If no specific rows are selected, sum the entire column
        if selected_rows is None:
            return df[column_name].sum()
        
        # If specific rows are provided, sum the values at those rows
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
    if student_name in df['Student Name'].values:  # Assuming 'Student Name' column exists
        student_row = df[df['Student Name'] == student_name]
        # Assuming attendance columns are all non-numeric and start from the second column
        attendance_columns = df.columns[1:]  # Skip the 'Student Name' column
        
        # Count 'P' for present days
        attendance = student_row[attendance_columns].apply(lambda x: x == 'P').sum(axis=1).values[0]
        return attendance
    else:
        print(f"Student '{student_name}' not found in the data.")
        return None

def calculate_defaulter(df, student_name, threshold=0.5):
    """Determine if a student is a defaulter based on attendance."""
    if student_name in df['Student Name'].values:
        student_row = df[df['Student Name'] == student_name]
        # Assuming attendance columns are all non-numeric and start from the second column
        attendance_columns = df.columns[1:]  # Skip the 'Student Name' column
        
        # Count 'A' for absent days
        total_days = len(attendance_columns)
        absences = student_row[attendance_columns].apply(lambda x: x == 'A').sum(axis=1).values[0]
        
        # Calculate the absence rate
        absence_rate = absences / total_days
        
        if absence_rate > threshold:
            return True  # Student is a defaulter
        else:
            return False  # Student is not a defaulter
    else:
        print(f"Student '{student_name}' not found in the data.")
        return None

def calculate_percentage(df, student_name):
    """Calculate the percentage of a student based on their marks."""
    if student_name in df['Student Name'].values:
        student_row = df[df['Student Name'] == student_name]
        
        # Identify the numeric columns (marks columns)
        score_columns = df.select_dtypes(include='number').columns
        
        # Sum the marks and calculate the percentage
        total_marks = student_row[score_columns].sum(axis=1).values[0]
        max_marks = len(score_columns) * 100  # Assuming each subject has a maximum score of 100
        percentage = (total_marks / max_marks) * 100
        return percentage
    else:
        print(f"Student '{student_name}' not found in the data.")
        return None

def main():
    # Ask user for the Excel file path
    file_path = input("Enter the path to the Excel file: ")

    # Read the Excel file
    df = read_excel_file(file_path)
    if df is None:
        return

    print("\nData in the Excel file:")
    print(df)

    # Ask user whether they want to sum a row, column, calculate attendance, check defaulter status, or calculate percentage
    choice = input("\nDo you want to add values of a row, column, calculate attendance, check defaulter status, or calculate percentage? (Enter 'row', 'column', 'attendance', 'defaulter', or 'percentage'): ").strip().lower()

    if choice == 'row':
        row_index = int(input("Enter the row index to sum (starting from 0): "))
        
        # Ask for specific columns to sum in the row
        selected_columns_input = input("Enter the column names to sum (comma-separated, or press Enter to sum the entire row): ").strip()
        
        if selected_columns_input:
            selected_columns = [x.strip() for x in selected_columns_input.split(',')]
        else:
            selected_columns = None
        
        result = add_row(df, row_index, selected_columns)
        if result is not None:
            if selected_columns:
                print(f"Sum of the selected cells in row {row_index}: {result}")
            else:
                print(f"Sum of the entire row {row_index}: {result}")
    elif choice == 'column':
        column_name = input("Enter the column name to sum: ")
        
        # Ask for specific rows to sum in the column
        selected_rows_input = input("Enter the row indices to sum (comma-separated, or press Enter to sum the entire column): ").strip()
        
        if selected_rows_input:
            # Convert the input to a list of integers (row indices)
            try:
                selected_rows = [int(x.strip()) for x in selected_rows_input.split(',')]
            except ValueError:
                print("Invalid input. Please enter valid row indices.")
                return
        else:
            # If no specific rows are provided, sum the entire column
            selected_rows = None
        
        result = add_column(df, column_name, selected_rows)
        if result is not None:
            if selected_rows:
                print(f"Sum of the selected rows in column '{column_name}': {result}")
            else:
                print(f"Sum of the entire column '{column_name}': {result}")
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
