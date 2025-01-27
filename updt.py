import pandas as pd

class ExcelSheetManager:
    def __init__(self):
        self.dataframe = pd.DataFrame()

    def create_sheet(self, rows):
        # Initialize a DataFrame with named columns
        self.dataframe = pd.DataFrame(index=range(rows), columns=["Name", "Roll No", "Div"])
        print(f"Created a sheet with {rows} rows and 3 columns: Name, Roll No, Div.")

    def enter_data(self):
        print("Enter data for the sheet row by row. Type 'done' to skip filling the rest of a row.")
        for row in range(len(self.dataframe)):
            for col in self.dataframe.columns:
                value = input(f"Enter value for {col} (Row {row + 1}): ")
                if value.lower() == 'done':
                    break
                self.dataframe.at[row, col] = value

    def display_sheet(self):
        print("\nCurrent Sheet:")
        print(self.dataframe)

    def save_to_excel(self, filename):
        if not filename.endswith(".xlsx"):
            filename += ".xlsx"
        
        try:
            self.dataframe.to_excel(filename, index=False, engine='openpyxl')
            print(f"Sheet saved to {filename}.")
        except Exception as e:
            print(f"Error saving file: {e}")

    def edit_existing_sheet(self, filename):
        try:
            # Load the existing Excel sheet
            self.dataframe = pd.read_excel(filename, engine='openpyxl')
            print("Loaded the existing Excel sheet.")
            self.display_sheet()
        except FileNotFoundError:
            print(f"Error: The file '{filename}' does not exist.")
            return
        except Exception as e:
            print(f"Error loading file: {e}")
            return

        # Editing the content
        print("Enter the row and column to edit the data (1-based index). Type 'done' to exit.")
        while True:
            row = input("Enter row number to edit (or 'done' to finish): ")
            if row.lower() == 'done':
                break
            col = input("Enter column name to edit: ")
            if col not in self.dataframe.columns:
                print("Invalid column name. Please try again.")
                continue
            try:
                row = int(row) - 1  # Convert to 0-based index
                if row < 0 or row >= len(self.dataframe):
                    print("Row out of range. Please try again.")
                    continue
            except ValueError:
                print("Invalid row number. Please enter a valid number.")
                continue
            
            # Get new value
            new_value = input(f"Enter new value for cell ({row + 1}, {col}): ")
            self.dataframe.at[row, col] = new_value
            print("Value updated successfully.")
            self.display_sheet()

        # Save the changes
        save_choice = input("Do you want to save the changes? (yes/no): ")
        if save_choice.lower() == 'yes':
            self.save_to_excel(filename)
        else:
            print("Changes discarded.")

# Main execution
if __name__ == "__main__":
    manager = ExcelSheetManager()

    action = input("Do you want to create a new sheet or edit an existing one? (new/edit): ").strip().lower()

    if action == 'new':
        rows = int(input("Enter the number of rows: "))
        manager.create_sheet(rows)
        manager.enter_data()
        manager.display_sheet()

        save_choice = input("Do you want to save this sheet to an Excel file? (yes/no): ")
        if save_choice.lower() == 'yes':
           filename = input("Enter the filename (with or without .xlsx extension): ")
           manager.save_to_excel(filename)
    elif action == 'edit':
        filename = input("Enter the filename of the existing Excel sheet: ").strip()
        manager.edit_existing_sheet(filename)
    else:
        print("Invalid choice. Exiting.")

        