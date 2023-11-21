import sqlite3
import pandas as pd
import re
import json

def perform_data_quality_checks(json_file_path, database_path='data.db'):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    data_df = pd.DataFrame(data)

    correct_data = []
    incorrect_data = []

    for index, row in data_df.iterrows():
        is_valid = True
        issues = []

        # Check for null values
        if row.isnull().any():
            is_valid = False
            issues.append("Contains null values")

        # Validate phone number format
        phone_number = str(row['PhoneNumber'])
        if not re.match(r'^\d{3}-\d{3}-\d{4}$', phone_number):
            is_valid = False
            issues.append("Invalid phone number format")

        # Validate data types and other constraints
        if not (isinstance(row['ID'], int) and row['ID'] > 0):
            is_valid = False
            issues.append("Invalid ID")

        dob = str(row['DateOfBirth'])
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', dob):
            is_valid = False
            issues.append("Invalid date format")

        if is_valid:
            correct_data.append(row)
        else:
            row['Issues'] = ', '.join(issues)
            incorrect_data.append(row)

    conn = sqlite3.connect(database_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS passed_data (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            DateOfBirth DATE,
            PhoneNumber TEXT
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS failed_data (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            DateOfBirth DATE,
            PhoneNumber TEXT,
            Issues TEXT
        )
    ''')

    passed_data_series = pd.DataFrame(correct_data)
    passed_data_series.to_sql('passed_data', conn, index=False, if_exists='replace')

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM passed_data')
    print("Passed data in db")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    failed_data_series = pd.DataFrame(incorrect_data)
    failed_data_series.to_sql('failed_data', conn, index=False, if_exists='replace', chunksize=1000)

    cursor.execute('SELECT * FROM failed_data')
    print("Failed data in db")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    print("Successfully inserted into db")
    conn.close()

# Usage
# Replace 'your_json_file.json' with your actual file path
perform_data_quality_checks('employee.json')
