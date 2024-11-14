import customtkinter
from tkinter import ttk  # Assuming Treeview from tkinter
from crud_operations import fetch_all_data, insert_data, update_data, delete_data
from ui_components import create_table_display

class LibraryApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("1200x600")

        # Sidebar for table navigation
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.crud_button_frame = customtkinter.CTkFrame(self)
        self.crud_button_frame.grid(row=1, column=1, sticky="ew")

        # Sidebar buttons for switching between tables
        table_names = ["Admins", "Members", "Publishers", "Authors", "Genres", "Books", "Loans", "Fines", "Reservations"]
        for idx, table in enumerate(table_names):
            btn = customtkinter.CTkButton(
                self.sidebar_frame, text=table, command=lambda t=table: self.load_table_data(t)
            )
            btn.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")

        # Initialize main display
        self.current_table = None
        self.form_entries = {}

    def load_table_data(self, table_name):
        """Loads and displays data for a specified table."""
        self.current_table = table_name
        columns, data = fetch_all_data(table_name)

        # Clear previous widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Display table
        if data:
            table_frame = create_table_display(self.main_frame, data, columns)
            table_frame.pack(fill="both", expand=True)

        # Update CRUD buttons
        self.update_crud_buttons()

    def update_crud_buttons(self):
        """Creates and displays CRUD buttons."""
        for widget in self.crud_button_frame.winfo_children():
            widget.destroy()

        if self.current_table:
            create_btn = customtkinter.CTkButton(
                self.crud_button_frame, text="Create", command=self.create_record
            )
            create_btn.grid(row=0, column=0, padx=5, pady=5)
            update_btn = customtkinter.CTkButton(
                self.crud_button_frame, text="Update", command=self.update_record
            )
            update_btn.grid(row=0, column=1, padx=5, pady=5)
            delete_btn = customtkinter.CTkButton(
                self.crud_button_frame, text="Delete", command=self.delete_record
            )
            delete_btn.grid(row=0, column=2, padx=5, pady=5)

    def create_record(self):
        """Opens a new form window for creating a record for the current table."""
        if not self.current_table:
            return

        form_window = customtkinter.CTkToplevel(self)
        form_window.title(f"Create Record for {self.current_table}")
        form_window.geometry("400x300")

        columns, _ = fetch_all_data(self.current_table)

        entry_widgets = {}
        for idx, column in enumerate(columns):
            label = customtkinter.CTkLabel(form_window, text=column)
            label.grid(row=idx, column=0, padx=10, pady=5)
            entry = customtkinter.CTkEntry(form_window)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_widgets[column] = entry

        submit_btn = customtkinter.CTkButton(
            form_window,
            text="Submit",
            command=lambda: self.submit_create_form(entry_widgets, form_window)
        )
        submit_btn.grid(row=len(columns), column=0, columnspan=2, pady=10)

    def submit_create_form(self, entry_widgets, form_window):
        """Handles form submission and data insertion."""
        try:
            values = [entry.get().strip() for entry in entry_widgets.values()]

            if any(value == "" for value in values):
                raise ValueError("All fields must be filled.")

            insert_data(self.current_table, values)
            success_label = customtkinter.CTkLabel(form_window, text="Record created successfully!", fg_color="green")
            success_label.grid(row=len(entry_widgets) + 1, column=0, columnspan=2)
            form_window.after(1500, form_window.destroy)
            self.load_table_data(self.current_table)

        except ValueError as ve:
            error_label = customtkinter.CTkLabel(form_window, text=f"Error: {ve}", fg_color="red")
            error_label.grid(row=len(entry_widgets) + 1, column=0, columnspan=2)

        except Exception as e:
            error_label = customtkinter.CTkLabel(form_window, text=f"Failed to create record: {e}", fg_color="red")
            error_label.grid(row=len(entry_widgets) + 1, column=0, columnspan=2)

    def update_record(self):
        """Displays a form for updating a record."""
        if not self.current_table:
            print("No table selected.")
            return

        selected_record = self.get_selected_record()
        if not selected_record:
            print("No record selected for update.")
            return

        update_window = customtkinter.CTkToplevel(self)
        update_window.title(f"Update Record in {self.current_table}")
        update_window.geometry("400x400")

        columns, _ = fetch_all_data(self.current_table)
        form_entries = {}

        for i, column in enumerate(columns):
            label = customtkinter.CTkLabel(update_window, text=column)
            label.grid(row=i, column=0, padx=5, pady=5)
            entry = customtkinter.CTkEntry(update_window)
            entry.insert(0, selected_record[i])
            entry.grid(row=i, column=1, padx=5, pady=5)
            form_entries[column] = entry

        submit_btn = customtkinter.CTkButton(
            update_window,
            text="Submit",
            command=lambda: self.submit_update_form(form_entries, update_window)
        )
        submit_btn.grid(row=len(columns), column=0, columnspan=2, pady=10)

    def submit_update_form(self, form_entries, window):
        """Submits the updated data to the database."""
        try:
            values = [entry.get() for entry in form_entries.values()]
            condition = f"id = {values[0]}"
            columns = list(form_entries.keys())[1:]
            update_data(self.current_table, columns, values[1:], condition)
            window.destroy()
            self.load_table_data(self.current_table)
            print("Record updated successfully!")
        except Exception as e:
            print(f"Failed to update record: {e}")

    def delete_record(self):
        """Handles record deletion for the current table."""
        if not self.current_table:
            print("No table selected.")
            return

        selected_record = self.get_selected_record()
        if not selected_record:
            print("No record selected for deletion.")
            return

        try:
            condition = f"id = {selected_record[0]}"
            delete_data(self.current_table, condition)
            self.load_table_data(self.current_table)
            print("Record deleted successfully!")
        except Exception as e:
            print(f"Failed to delete record: {e}")

    def get_selected_record(self):
        """Retrieves the currently selected record from the Treeview table."""
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, customtkinter.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Treeview):
                        selected_items = child.selection()
                        if selected_items:
                            return child.item(selected_items[0], "values")
        
        # If we get here, either no selection was made or no table exists
        print("Please select a record first.")
        return None
