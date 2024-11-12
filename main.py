import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connect to the MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQLpassword4321",
            database="LibraryDB"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database connection failed: {err}")
        return None

# Function to view all records in a selected table
def view_records(table_name):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            
            # Clear the treeview
            for i in tree.get_children():
                tree.delete(i)
            
            # Display table records
            for record in records:
                tree.insert('', 'end', values=record)

            # Get column names
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [col[0] for col in cursor.fetchall()]
            tree["columns"] = columns
            tree["show"] = "headings"
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching data: {err}")
        finally:
            cursor.close()
            conn.close()

# Function to add a record to a selected table
def add_record(table_name, entries):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            columns = ", ".join(entries.keys())
            placeholders = ", ".join(["%s"] * len(entries))
            values = tuple(entry.get() for entry in entries.values())
            
            cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
            conn.commit()
            messagebox.showinfo("Success", f"Record added to {table_name} successfully!")
            view_records(table_name)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error adding record: {err}")
        finally:
            cursor.close()
            conn.close()

# Function to delete a selected record
def delete_record(table_name, primary_key, pk_value):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {table_name} WHERE {primary_key} = %s", (pk_value,))
            conn.commit()
            messagebox.showinfo("Success", f"Record deleted from {table_name} successfully!")
            view_records(table_name)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error deleting record: {err}")
        finally:
            cursor.close()
            conn.close()

# Main application window
root = tk.Tk()
root.title("Library Database Management")
root.geometry("1000x600")

# Table selection dropdown
table_label = tk.Label(root, text="Select Table:")
table_label.pack(pady=5)

table_combo = ttk.Combobox(root, values=["Admins", "Fines", "Reservations", "Loans", "Members", "Books", "Publishers", "Authors", "Genres"])
table_combo.pack(pady=5)

# View button
view_button = tk.Button(root, text="View Records", command=lambda: view_records(table_combo.get()))
view_button.pack(pady=5)

# Treeview widget for displaying data
tree = ttk.Treeview(root)
tree.pack(pady=20, fill="both", expand=True)

# Add record section
add_frame = tk.Frame(root)
add_frame.pack(pady=10)

def open_add_window():
    table_name = table_combo.get()
    if not table_name:
        messagebox.showerror("Error", "Please select a table first.")
        return
    
    add_window = tk.Toplevel(root)
    add_window.title(f"Add Record to {table_name}")
    add_window.geometry("400x400")
    
    entries = {}
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = cursor.fetchall()
            
            for i, (col_name, col_type, *_rest) in enumerate(columns):
                if "int" in col_type.lower() or "varchar" in col_type.lower() or "date" in col_type.lower():
                    tk.Label(add_window, text=f"{col_name}:").grid(row=i, column=0, padx=5, pady=5)
                    entry = tk.Entry(add_window)
                    entry.grid(row=i, column=1, padx=5, pady=5)
                    entries[col_name] = entry

            submit_button = tk.Button(add_window, text="Add Record", command=lambda: add_record(table_name, entries))
            submit_button.grid(row=len(columns), column=1, pady=10)
        
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching columns: {err}")
        finally:
            cursor.close()
            conn.close()

# Button to open add record window
add_button = tk.Button(root, text="Add Record", command=open_add_window)
add_button.pack(pady=5)

root.mainloop()
