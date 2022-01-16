from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import User, UserAuth
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
    check_user_phone = coll_name.find_one({"phone": credentials.username})
    check_user_email = coll_name.find_one({"email": credentials.username})
    if check_user_phone or check_user_email:
        check_password = coll_name.find_one({"password": credentials.password})
        if check_password:
            return {"Response": "User Successfully Authenticated!"}
        else:
            raise HTTPException(status_code=401, detail="User does not exists or incorrect password", headers={'WWW-Authenticate': 'Basic'},)
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

# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     fakeDB[item_id] = item
#     return {"item_name": item.name, "item_id": item_id}

# @app.delete("/items/{item_id}")
# def delete_item(item_id: int):
#     for key in fakeDB.keys():
#         if item_id == key:
#             del fakeDB[item_id]
#             return{item_id," item deleted successfully!"}
#     raise HTTPException(status_code=404, detail="Item not found for deletion")