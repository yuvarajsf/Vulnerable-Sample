from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import sqlite3

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify specific origins instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database connection
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')
conn.commit()

# Functions to work with the database
def get_user(username: str, password: str = None):
    try:
        if password is None:
            query = "SELECT * FROM users WHERE username="+"'"+username+"'"
        else:
            query = "SELECT * FROM users WHERE username="+"'"+username+"' AND password='"+password+"'"
        print(query)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as ex: 
        return ex

def create_user(username: str, password: str):
    query = "INSERT INTO users (username, password) VALUES ('" + username + "', '"+password+"')"
    cursor.execute(query)
    print(query)
    conn.commit()
    return {"username": username}

# Routes
@app.post("/register")
async def register(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    user = get_user(username)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    create_user(username, password)
    return {"message": "User created successfully"}

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    user = get_user(username, password)
    if type(user) == list:
        if user:
            return {"message": "Login successful", "data": user}
    raise HTTPException(status_code=401, detail= json.dumps(user.args))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=1234)