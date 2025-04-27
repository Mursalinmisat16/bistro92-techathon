from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime



class Order(SQLModel, table=True):
    
    __tablename__ = 'orders'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    table_number: int
    created_at: datetime
    status: str = Field(default="pending")

    items: List["OrderItem"] = Relationship(back_populates="order")




class OrderItem(SQLModel, table=True):
    
    __tablename__ = 'order_items'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    item_name: str
    quantity: int

    order: Optional["Order"] = Relationship(back_populates="items")





