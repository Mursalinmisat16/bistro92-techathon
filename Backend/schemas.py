from typing import Dict
from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    table: int
    order: Dict[str, int]
    

class OrderItemRead(BaseModel):
    item_name: str
    quantity: int



class OrderRead(BaseModel):
    order_id: int
    table_number: int
    created_at: datetime
    status: str
    items: list[OrderItemRead]
