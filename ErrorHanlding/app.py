from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import traceback
import datetime

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

users = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 35},
    {"id": 3, "name": "Charlie", "age": 25},
]

logging.basicConfig(filename='log.txt')

@app.get("/user/{user_id}")
async def get_user(user_id):
    try:
        for user in users:
            if user["id"] == int(user_id):
                #logging the success response
                msg = str(datetime.datetime.now()) + "--> userId: " + user_id + "\nMethod: "+ get_user.__name__ + "\n" + "-"*50 + "\n"
                logging.error(msg)
                
                return {"status_code": 200, "data": user}
        return {"status_code":404, "data":"User not found"}
    
    except Exception as e:
        #genric error logging
        # logging.error(f"Exception occurred: {str(e)}")
        # return {"status_code": 500, "exe": str(e), "data": traceback.format_exc()}

        #example proper logging
        msg = str(datetime.datetime.now()) + "--> Error: " + str(e) + "\nMethod: "+ get_user.__name__ + "\nStackTrace: " + traceback.format_exc() + "\n" + "-"*50 + "\n"
        logging.error(msg)
        return {"status_code": 500, "data": "Internal Server Error"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=5000)