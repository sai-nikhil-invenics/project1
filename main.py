import sqlite3

# Connect to SQLite database (this will create a new file called 'dq_database.db')
conn = sqlite3.connect('data.db.db')

# Create tables for passed and failed data
conn.execute('''
CREATE TABLE PassedData (
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    DateOfBirth DATE,
    PhoneNumber TEXT
);
''')

conn.execute('''
CREATE TABLE FailedData (
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    DateOfBirth DATE,
    PhoneNumber TEXT,
    FailedReason TEXT
);
''')
cursor = conn.cursor()
cursor.execute('SELECT * FROM  PassedData')
# Commit and close connection
conn.commit()
conn.close()

