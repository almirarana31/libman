import customtkinter
from tkinter import ttk

def create_table_display(master, data, columns):
    """Creates a table display using Treeview with selection capability."""
    # Create a frame to hold the table
    frame = customtkinter.CTkFrame(master)
    frame.pack(fill="both", expand=True)

    # Create the Treeview
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    
    # Configure scrollbars
    y_scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
    x_scrollbar = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    # Set column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, minwidth=100, width=150)  # Adjust width as needed

    # Insert data
    if data:
        for row in data:
            tree.insert('', 'end', values=row)
    else:
        tree.insert('', 'end', values=['No data available'] * len(columns))

    # Layout
    tree.grid(row=0, column=0, sticky='nsew')
    y_scrollbar.grid(row=0, column=1, sticky='ns')
    x_scrollbar.grid(row=1, column=0, sticky='ew')

    # Configure grid weights
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    return frame
