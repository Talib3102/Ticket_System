import re

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Ticket
from fastapi.responses import FileResponse
from schemas import (
    TicketCreate,TicketCreateResponse, TicketResponse
)


def generate_ticket_id(db: Session) -> str:
    """Return the next sequential ID, ignoring legacy alphanumeric IDs."""
    ticket_ids = db.query(Ticket.ticket_id).all()
    numeric_ids = (
        int(match.group(1))
        for (ticket_id,) in ticket_ids
        if (match := re.fullmatch(r"TKT-(\d+)", ticket_id))
    )
    next_number = max(numeric_ids, default=0) + 1
    return f"TKT-{next_number:03d}"

def build_ticket_response(t: Ticket) -> TicketResponse:
    
    return TicketResponse(
        id=str(t.id),
        ticket_id=t.ticket_id,
        customer_name=t.customer_name,
        customer_email=t.customer_email,
        subject=t.subject,
        status=t.status,
        priority=t.priority,
        created_at=t.created_at,
        updated_at=t.updated_at
    )


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/create")
def home():
    return FileResponse("static/create.html")  # Serve the HTML file


#CREATE TICKET  
@app.post("/tickets", response_model=TicketCreateResponse, status_code=201)
def create_ticket(ticket_data: TicketCreate, db: Session = Depends(get_db)):

    ticket_id = generate_ticket_id(db)
 
    new_ticket = Ticket(
        ticket_id=ticket_id,
        customer_name=ticket_data.customer_name.strip(),
        customer_email=ticket_data.customer_email.strip().lower(),
        subject=ticket_data.subject.strip(),
        description=ticket_data.description.strip(),
        status="Open",
        priority=ticket_data.priority or "Medium"
    )
 
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
 
    return TicketCreateResponse(
        ticket_id=new_ticket.ticket_id,
        created_at=new_ticket.created_at
    )
