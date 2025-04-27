from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime


from database import get_db
from models import Order, OrderItem
import schemas
router = APIRouter(tags=["Order"])
@router.post("/order")
def create_order(order_data: schemas.OrderCreate, session: Session = Depends(get_db)):
    table_number = order_data.table  # access attributes
    order_items = order_data.order   # access attributes

    order = Order(table_number=table_number, created_at=datetime.now())
    session.add(order)
    session.commit()
    session.refresh(order)  # Now order.id is available

    for item_name, quantity in order_items.items():
        order_item = OrderItem(
            order_id=order.id,
            item_name=item_name,
            quantity=quantity
        )
        session.add(order_item)

    session.commit()
    return {"message": "Order created successfully", "order_id": order.id}



@router.get("/orders") # , response_model=list[schemas.OrderRead]
def get_all_orders(session: Session = Depends(get_db)):
    orders = session.exec(select(Order).order_by(Order.id.desc())).all()
    result = []

    for order in orders:
        items = session.exec(
            select(OrderItem).where(OrderItem.order_id == order.id)
        ).all()

        order_data = schemas.OrderRead(
            order_id=order.id,
            table_number=order.table_number,
            created_at=order.created_at,
            status=order.status,
            items=[
                schemas.OrderItemRead(
                    item_name=item.item_name,
                    quantity=item.quantity
                ) for item in items
            ]
        )
        result.append(order_data)

    return result



@router.patch("/order/{order_id}/serve")
def serve_order(order_id: int, session: Session = Depends(get_db)):
    order = session.get(Order, order_id)
    if not order:
        return {"error": "Order not found"}

    order.status = "served"
    session.add(order)
    session.commit()
    session.refresh(order)
    return {"message": "Order marked as served"}


