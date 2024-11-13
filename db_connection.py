import mysql.connector

def create_connection():
    """Establishes a connection to the MySQL database."""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your DB username
        password='MySQLpassword4321',  # Replace with your DB password
        database='LibraryDB'
    )
    return connection
