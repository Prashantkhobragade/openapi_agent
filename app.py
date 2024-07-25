
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Pydantic model for request body
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., title="The ID of the item to get", ge=1),
    q: Optional[str] = Query(None, max_length=50)
):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
def update_item(
    item_id: int = Path(..., title="The ID of the item to update", ge=1),
    item: Item = Body(..., embed=True)
):
    return {"item_id": item_id, "item": item}

@app.delete("/items/{item_id}")
def delete_item(
    item_id: int = Path(..., title="The ID of the item to delete", ge=1)
):
    return {"item_id": item_id, "message": "Item deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

"""
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

"""