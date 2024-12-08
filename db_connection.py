import mysql.connector

def create_connection():
    """Establishes a connection to the MySQL database."""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your DB username
        password='drowssaPtooR',  # Replace with your DB password
        database='librarymanagement'
    )
    return connection
