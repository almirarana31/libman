import customtkinter

def create_table_display(master, data, columns):
    """Creates a table-like display in the GUI."""
    frame = customtkinter.CTkFrame(master)
    if columns:
        # Create header
        for col_num, col_name in enumerate(columns):
            label = customtkinter.CTkLabel(frame, text=col_name, font=("Arial", 12, "bold"))
            label.grid(row=0, column=col_num, padx=5, pady=5)

        # Create data rows
        for row_num, row_data in enumerate(data, start=1):
            for col_num, item in enumerate(row_data):
                label = customtkinter.CTkLabel(frame, text=item)
                label.grid(row=row_num, column=col_num, padx=5, pady=5)
    else:
        label = customtkinter.CTkLabel(frame, text="No data available")
        label.grid(row=0, column=0)

    return frame
