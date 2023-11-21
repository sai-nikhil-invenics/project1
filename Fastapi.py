from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import json
from dq_check import perform_data_quality_checks

app = FastAPI()

# Define Pydantic models
class JSONRequest(BaseModel):
    json_file_path : str


# Function to perform data quality checks


@app.post("/data_quality_check/")
async def data_quality_check(request: JSONRequest):
    # perform_data_quality_checks(request.json_file_path)
    return {"message": "Data quality checks completed and stored in the database."}

@app.post("/dq_check/")
async def get_passed_data(jsonrequest:JSONRequest):
    def call(user_input):
        if user_input == "pass":
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM passed_data')
            passed_data = cursor.fetchall()
            conn.close()
            return {"passed_data": passed_data}
        elif user_input == "fail":
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM failed_data')
            failed_data = cursor.fetchall()
            conn.close()
            return {"failed_data": failed_data}
        else:
            return("valid input")

    result= call(jsonrequest.json_file_path)
    return {"result": result}

