import sqlite3

def view_table_data(table_name):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('dq_database.db')

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve all rows from the specified table
        cursor.execute(f"SELECT * FROM {table_name}")

        # Fetch all the rows
        rows = cursor.fetchall()

        # Print the column names
        column_names = [description[0] for description in cursor.description]
        print(column_names)

        # Print the data
        for row in rows:
            print(row)

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error viewing table data: {str(e)}")

if __name__ == '__main__':
    # View data in the PassedData table
    print("Viewing data in PassedData table:")
    view_table_data('PassedData')

    # View data in the FailedData table
    print("\nViewing data in FailedData table:")
    view_table_data('FailedData')
