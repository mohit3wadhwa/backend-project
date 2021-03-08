from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

fakeDB = {}

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    for key in fakeDB.keys():
        if item_id == key:
            #return{"item_id": item_id, "value": value}
            return {"item": fakeDB[key]}
    #return{"no items found"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items")
def read_all_items():
    if not fakeDB:
        raise HTTPException(status_code=404, detail="No Items found")
    else:
        return fakeDB


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    fakeDB[item_id] = item
    return {"item_name": item.name, "item_id": item_id}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for key in fakeDB.keys():
        if item_id == key:
            del fakeDB[item_id]
            return{item_id," item deleted successfully!"}
    raise HTTPException(status_code=404, detail="Item not found for deletion")