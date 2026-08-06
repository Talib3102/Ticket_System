from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Ticket
from schemas import TicketCreate
from fastapi.responses import FileResponse


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/create")
def home():
    return FileResponse("static/create.html")  # Serve the HTML file


@app.post("/tickets/", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket_data: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = Ticket(
        customer_name=ticket_data.customer_name,
        customer_email=ticket_data.customer_email,
        subject=ticket_data.subject,
        description=ticket_data.description,
        priority=ticket_data.priority
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "message": "Ticket created successfully",
        "ticket_id": new_ticket.id,
        "status": new_ticket.status
    }