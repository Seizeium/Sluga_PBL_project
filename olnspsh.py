import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetManager:
    def __init__(self, json_keyfile, sheet_name):
        """Initialize Google Sheets API authentication and open the sheet."""
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                      "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(sheet_name).sheet1  
        self.headers = []
        print(f"Connected to Google Sheet: {sheet_name}")

    def create_sheet(self):
        file_name = input("Enter a file name : ")
        email = input("Enter the email : ")
        new_file = self.client.create(file_name)
        new_file.share(email, perm_type='user', role='writer')
        self.sheet = new_file.sheet1

        i =  int(input("Enter the number of Column : "))
        for o in range(i):
            n = input(f"Enter {o + 1} Column : ")
            self.headers.append(n)
        self.sheet.append_row(self.headers)
        print("Created Google Sheet with headers:", self.headers)

    def enter_data(self):
        print("Enter data for the sheet. Type 'done' to stop.")
        
        while True:
            row_data = []
            for i in range(len(self.headers)):
                val = input(f"Enter the values for {self.headers[i]} : ")
                if val.lower() == "done":
                    return
                
                row_data.append(val)
            self.sheet.append_row(row_data)  
            print("Row added successfully.")

    def display_sheet(self):
        """Fetches and displays the current sheet data."""
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        print("\nCurrent Google Sheet Data:\n", df)

    def edit_existing_sheet(self):
        """Allows editing of existing data."""
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)

        print("\nCurrent Google Sheet Data:\n", df)

        while True:
            row_num = input("Enter the row number to edit (1-based index, or 'done' to finish): ")
            if row_num.lower() == "done":
                break
            try:
                row_num = int(row_num)
                if row_num <= 0 or row_num > len(df):
                    print("Invalid row number. Try again.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue

            col_name = input("Enter column name to edit: ")
            if col_name not in df.columns:
                print("Invalid column name. Try again.")
                continue

            new_value = input(f"Enter new value for {col_name} in row {row_num}: ")
            self.sheet.update_cell(row_num + 1, df.columns.get_loc(col_name) + 1, new_value)
            print("Value updated successfully.")

    def delete_data(self):
        """Deletes a specific row or column."""
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)

        print("\nCurrent Google Sheet Data:\n", df)

        while True:
            choice = input("Do you want to delete a row or column? (row/column/done): ").strip().lower()
            if choice == "done":
                break
            elif choice == "row":
                row_num = int(input("Enter the row number to delete (1-based index): "))
                self.sheet.delete_rows(row_num)
                print(f"Row {row_num} deleted successfully.")
            elif choice == "column":
                col_name = input("Enter the column name to delete: ").strip()
                if col_name in df.columns:
                    col_idx = df.columns.get_loc(col_name) + 1
                    self.sheet.update_cell(1, col_idx, "")  # Clears column header
                    for i in range(2, len(df) + 2):
                        self.sheet.update_cell(i, col_idx, "")  # Clears column data
                    print(f"Column '{col_name}' deleted successfully.")
            else:
                print("Invalid choice. Please enter 'row', 'column', or 'done'.")
    def add_to_specific_row(self):
        """Adds data to a specific row and column."""
        row_num = int(input("Enter row num : "))
        column_name = (input("Enter column name : "))
        new_value = input("Enter new value to be added : ")

        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        
        if column_name not in df.columns:
            print("Invalid column name.")
            return
        
        df.at[row_num - 1, column_name] = new_value  # Adjusting for 0-based index
        # Update the Google Sheet
        self.sheet.update_cell(row_num, df.columns.get_loc(column_name) + 1, new_value)
        print(f"Row {row_num}, Column '{column_name}' updated with '{new_value}'.")

    def add_to_specific_column(self, column_name, values_list):
        """Adds or updates a specific column with a list of values."""
        # Fetching current sheet data
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)

        if column_name not in df.columns:
            print(f"Column '{column_name}' not found. Adding new column.")
            df[column_name] = values_list
        else:
            print(f"Updating existing column '{column_name}'.")
            df[column_name] = values_list
        
        # Update the entire column in Google Sheet
        for i, value in enumerate(values_list, start=2):  # start=2 because data starts from row 2 in Google Sheets
            self.sheet.update_cell(i, df.columns.get_loc(column_name) + 1, value)
        print(f"Column '{column_name}' updated with new values.")

if __name__ == "__main__":
    json_keyfile = r"C:\Users\Sneha\Downloads\SLUGA.04.json"
    sheet_name = "workspreadsheet"  

    manager = GoogleSheetManager(json_keyfile, sheet_name)
    action = input("Do you want to create a new sheet or edit an existing one? (new/edit): ").strip().lower()


    if action == "new":
        manager.create_sheet()
        manager.enter_data()
        manager.display_sheet()
    elif action == "edit":
        manager.edit_existing_sheet()
        delete_choice = input("Do you want to delete data from the sheet? (yes/no): ")
        if delete_choice.lower() == "yes":
            manager.delete_data()
    elif action == "add":
        manager.add_to_specific_row()
    else:
        print("Invalid choice. Exiting.")

        



