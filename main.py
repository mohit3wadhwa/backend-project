from ast import Delete
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import User, DeleteUser, UpdateUser
import pymongo
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
security = HTTPBasic()

def connect_db():
    try:
        client = pymongo.MongoClient(os.getenv('MONGODB_ATLAS_URI'), serverSelectionTimeoutMS=5000)
        print("DB connection successful")
    except Exception:
        print("Something is wrong while connecting to Database")
    
    db = client.get_database('userDB')
    coll = db["users"]
    return coll
    

@app.get("/")
def read_root():
    return {"Response": "API Works!"}


@app.get("/signin/")
def read_item(credentials: HTTPBasicCredentials = Depends(security)):
    coll_name = connect_db()
    check_user_phone = coll_name.find_one({"phone": credentials.username, "password": credentials.password})
    check_user_email = coll_name.find_one({"email": credentials.username, "password": credentials.password})
    if check_user_phone or check_user_email:
        return {"Response": "User Successfully Authenticated!"}
    else:
        raise HTTPException(status_code=401, detail="User does not exists or incorrect password", headers={'WWW-Authenticate': 'Basic'},)
    

@app.post("/signup/", status_code=201)
def insert_user(user: User):
    coll_name = connect_db()
    check_user_phone = coll_name.find_one({"phone": user.phone})
    check_user_email = coll_name.find_one({"email": user.email})
    if not check_user_phone and not check_user_email:
        _id = coll_name.insert_one(user.__dict__).inserted_id
        return {"Response": "User " + str(_id) + " created successfully!"}
    else:
        raise HTTPException(status_code=409, detail="Phone Number or Email already exists")

@app.put("/update/user/")
def update_user(user: UpdateUser):
    coll_name = connect_db()
    check_user = coll_name.find_one({"phone": user.phone, "password": user.password})
    if check_user:
        filter_query = {"phone": user.phone, "password": user.password}
        new_values = {"$set": user.__dict__}
        coll_name.update_one(filter_query, new_values)
        return {"Response": "User Successfully Updated!"}
    else:
        raise HTTPException(status_code=404, detail="User does not exists or incorrect password")


@app.delete("/delete/user/")
def delete_user(user: DeleteUser):
    coll_name = connect_db()
    check_user_phone = coll_name.find_one({"phone": user.username, "password": user.password})
    check_user_email = coll_name.find_one({"email": user.username, "password": user.password})
    if check_user_email:
        coll_name.delete_one({"email": user.username, "password": user.password})
        return {"Response": "User Deleted Successfully!"}
    elif check_user_phone:
        coll_name.delete_one({"phone": user.username, "password": user.password})
        return {"Response": "User Deleted Successfully!"}
    else:
        raise HTTPException(status_code=404, detail="User does not exists or incorrect password")
    