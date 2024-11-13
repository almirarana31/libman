from db_connection import create_connection

def fetch_all_data(table_name):
    """Fetches all data from a specified table."""
    conn = create_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return columns, result

def insert_data(table_name, columns, values):
    """Inserts data into a specified table."""
    conn = create_connection()
    cursor = conn.cursor()
    col_string = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table_name} ({col_string}) VALUES ({placeholders})"
    cursor.execute(query, values)
    conn.commit()
    conn.close()

def update_data(table_name, set_columns, values, condition):
    """Updates data in a specified table based on a condition."""
    conn = create_connection()
    cursor = conn.cursor()
    set_string = ', '.join([f"{col} = %s" for col in set_columns])
    query = f"UPDATE {table_name} SET {set_string} WHERE {condition}"
    cursor.execute(query, values)
    conn.commit()
    conn.close()

def delete_data(table_name, condition):
    """Deletes data from a specified table based on a condition."""
    conn = create_connection()
    cursor = conn.cursor()
    query = f"DELETE FROM {table_name} WHERE {condition}"
    cursor.execute(query)
    conn.commit()
    conn.close()
