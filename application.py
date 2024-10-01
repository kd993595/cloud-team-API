from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import os, uuid
import mysql.connector

app = FastAPI()

# Define the Pydantic model for request validation
class Preference(BaseModel):
    preference_id: int
    user_id: int
    food_id: int

class User(BaseModel):
    user_id: int


@app.post("/addPref")
async def add_pref(pref: Preference, response: Response):
    try:
        conn = mysql.connector.connect(
            # TODO use env var in AWS for security
            host=os.getenv('db_uri'),
            user=os.getenv('db_username'),
            password=os.getenv('db_password'),
            database=os.getenv('db_name')
        )
        cursor = conn.cursor()
        cursor.execute('''
               INSERT INTO preference (preference_id, user_id, food_id)
               VALUES (%s, %s, %s)
           ''', (pref.preference_id, pref.user_id, pref.food_id))
        conn.commit()
        conn.close()

        response.status_code = status.HTTP_201_CREATED
        return {"message": "Preference created successfully"}
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Preference creation unsuccessful"}

@app.post("/getPref")
async def get_pref(user: User, response: Response):
    try:
        conn = mysql.connector.connect(
            # TODO use env var in AWS for security
            host=os.getenv('db_uri'),
            user=os.getenv('db_username'),
            password=os.getenv('db_password'),
            database=os.getenv('db_name')
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM preference WHERE user_id = %s', (user.user_id,))
        results = cursor.fetchall()
        conn.close()
        response.status_code = status.HTTP_200_OK
        return {"message": "Preference retrieved successfully", "data": results}
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Database Query unsuccessful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
