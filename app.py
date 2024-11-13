import customtkinter
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
        """Handles record creation for the current table."""
        print(f"Create operation for {self.current_table}")

    def update_record(self):
        """Handles record update for the current table."""
        print(f"Update operation for {self.current_table}")

    def delete_record(self):
        """Handles record deletion for the current table."""
        print(f"Delete operation for {self.current_table}")
