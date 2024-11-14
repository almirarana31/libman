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
        form_window.geometry("800x600")  # Wider window to accommodate lookups

        # Create main container frames
        left_frame = customtkinter.CTkFrame(form_window)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Only create right frame for Books table
        if self.current_table == "Books":
            right_frame = customtkinter.CTkFrame(form_window)
            right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Create scrollable frame for form
        canvas = customtkinter.CTkCanvas(left_frame, height=400)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = customtkinter.CTkFrame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Get table columns
        columns, _ = fetch_all_data(self.current_table)
        
        entry_widgets = {}
        
        # Create form fields
        for idx, column in enumerate(columns):
            label = customtkinter.CTkLabel(scrollable_frame, text=column)
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="e")
            
            entry = customtkinter.CTkEntry(scrollable_frame, width=200)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            entry_widgets[column] = entry

        # Add reference tables for Books
        if self.current_table == "Books":
            # Fetch and display Authors
            authors_label = customtkinter.CTkLabel(right_frame, text="Available Authors:", font=("Arial", 12, "bold"))
            authors_label.pack(anchor="w", padx=10, pady=(10, 5))
            
            authors_data = fetch_all_data("Authors")
            authors_text = "\n".join([f"ID: {author[0]} - {author[1]}" for author in authors_data[1]])
            authors_textbox = customtkinter.CTkTextbox(right_frame, height=100, width=300)
            authors_textbox.pack(padx=10, pady=(0, 10), fill="x")
            authors_textbox.insert("1.0", authors_text)
            authors_textbox.configure(state="disabled")

            # Fetch and display Genres
            genres_label = customtkinter.CTkLabel(right_frame, text="Available Genres:", font=("Arial", 12, "bold"))
            genres_label.pack(anchor="w", padx=10, pady=(10, 5))
            
            genres_data = fetch_all_data("Genres")
            genres_text = "\n".join([f"ID: {genre[0]} - {genre[1]}" for genre in genres_data[1]])
            genres_textbox = customtkinter.CTkTextbox(right_frame, height=100, width=300)
            genres_textbox.pack(padx=10, pady=(0, 10), fill="x")
            genres_textbox.insert("1.0", genres_text)
            genres_textbox.configure(state="disabled")

            # Fetch and display Publishers
            publishers_label = customtkinter.CTkLabel(right_frame, text="Available Publishers:", font=("Arial", 12, "bold"))
            publishers_label.pack(anchor="w", padx=10, pady=(10, 5))
            
            publishers_data = fetch_all_data("Publishers")
            publishers_text = "\n".join([f"ID: {pub[0]} - {pub[1]}" for pub in publishers_data[1]])
            publishers_textbox = customtkinter.CTkTextbox(right_frame, height=100, width=300)
            publishers_textbox.pack(padx=10, pady=(0, 10), fill="x")
            publishers_textbox.insert("1.0", publishers_text)
            publishers_textbox.configure(state="disabled")

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Submit button at the bottom
        submit_frame = customtkinter.CTkFrame(form_window)
        submit_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        submit_btn = customtkinter.CTkButton(
            submit_frame,
            text="Submit",
            command=lambda: self.submit_create_form(entry_widgets, form_window)
        )
        submit_btn.pack(pady=5)

    def submit_create_form(self, entry_widgets, form_window):
        """Handles form submission and data insertion."""
        try:
            values = [entry.get().strip() for entry in entry_widgets.values()]

            if any(value == "" for value in values):
                raise ValueError("All fields must be filled.")

            # Insert the data
            insert_data(self.current_table, values)
            
            # Show success message
            success_frame = customtkinter.CTkFrame(form_window)
            success_frame.pack(fill="x", padx=10, pady=5)
            success_label = customtkinter.CTkLabel(
                success_frame, 
                text="Record created successfully!", 
                text_color="green"
            )
            success_label.pack()
            form_window.after(1500, form_window.destroy)
            self.load_table_data(self.current_table)

        except Exception as e:
            # Create a more user-friendly error message
            error_msg = str(e)
            if "foreign key constraint fails" in error_msg.lower():
                if "authorid" in error_msg.lower():
                    error_msg = "Error: The specified AuthorID does not exist in the Authors table."
                elif "genreid" in error_msg.lower():
                    error_msg = "Error: The specified GenreID does not exist in the Genres table."
                elif "publisherid" in error_msg.lower():
                    error_msg = "Error: The specified PublisherID does not exist in the Publishers table."
            
            # Show error in a contained frame
            error_frame = customtkinter.CTkFrame(form_window)
            error_frame.pack(fill="x", padx=10, pady=5)
            error_label = customtkinter.CTkLabel(
                error_frame,
                text=error_msg,
                text_color="red",
                wraplength=350
            )
            error_label.pack(pady=5)

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
            
            # Get the first column name (assuming it's the primary key)
            primary_key_column = list(form_entries.keys())[0]
            primary_key_value = values[0]
            
            # Create the WHERE clause using the actual column name
            condition = f"{primary_key_column} = {primary_key_value}"
            
            # Remove the primary key from the columns to update
            columns = list(form_entries.keys())[1:]
            
            # Update with all values except the primary key
            update_data(self.current_table, columns, values[1:], condition)
            
            # Show success message
            success_label = customtkinter.CTkLabel(window, text="Record updated successfully!", fg_color="green")
            success_label.grid(row=len(form_entries) + 1, column=0, columnspan=2)
            window.after(1500, window.destroy)
            self.load_table_data(self.current_table)
            
        except Exception as e:
            # Show error message in the form window
            error_label = customtkinter.CTkLabel(window, text=f"Failed to update record: {e}", fg_color="red")
            error_label.grid(row=len(form_entries) + 1, column=0, columnspan=2)

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
            # Get the columns for the current table
            columns, _ = fetch_all_data(self.current_table)
            # Use the first column as the primary key
            primary_key_column = columns[0]
            primary_key_value = selected_record[0]
            
            # Create the WHERE clause using the actual column name
            condition = f"{primary_key_column} = {primary_key_value}"
            
            # Perform the deletion
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
