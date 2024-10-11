from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import os, uuid
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

os.environ['db_uri'] = ''
os.environ['db_username'] = ''
os.environ['db_password'] = ''
app = FastAPI()

# List of allowed origins (domains that can make requests)
origins = [
    "http://localhost:8080",  # If your frontend runs on localhost:3000 (e.g., React app)
    "https://yourfrontend.com",  # Replace with your frontend domain
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origins that are allowed to access your API
    allow_credentials=True,  # Allow cookies and authentication
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers (authorization, content-type, etc.)
)

# Define the Pydantic model for request validation
class Preference(BaseModel):
    preference_id: int
    user_id: int
    food_id: int

class User(BaseModel):
    user_id: int

@app.get("/")
async def home():
    try:
        conn = mysql.connector.connect(
            # TODO use env var in AWS for security
            host=os.getenv('db_uri'),
            user=os.getenv('db_username'),
            password=os.getenv('db_password'),
            # database=os.getenv('db_name')
        )
        conn.close()
        return {"message": "DB Connected!"}
    except:
        return {"message": "Cannot Access DB"}

@app.post("/addPref")
async def add_pref(pref: Preference, response: Response):
    try:
        conn = mysql.connector.connect(
            # TODO use env var in AWS for security
            host=os.getenv('db_uri'),
            user=os.getenv('db_username'),
            password=os.getenv('db_password'),
            # database=os.getenv('db_name')
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
