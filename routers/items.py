# routers/items.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Определяем модель для товара
class Item(BaseModel):
    id: int = None
    name: str
    description: str = None
    price: float

# Временное хранилище товаров
items_db = [
    Item(id=1, name="Товар 1", description="Описание товара 1", price=10.0),
    Item(id=2, name="Товар 2", description="Описание товара 2", price=20.0)
]

# Чтение списка товаров
@router.get("/items/", response_model=List[Item])
async def read_items():
    return items_db

# Чтение конкретного товара по ID
@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
