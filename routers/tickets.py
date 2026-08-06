from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
from typing import Optional, List
 
from database import get_db
from models import Ticket, Note
from schemas import (
    TicketCreate
)
#CREATE TICKET  
@router.post("/", response_model=TicketCreateResponse, status_code=201)
def create_ticket(ticket_data: TicketCreate, db: Session = Depends(get_db)):

    ticket_id = generate_ticket_id(db)
 
    new_ticket = Ticket(
        ticket_id=ticket_id,
        customer_name=ticket_data.customer_name.strip(),
        customer_email=ticket_data.customer_email.strip().lower(),
        subject=ticket_data.subject.strip(),
        description=ticket_data.description.strip(),
        status="Open",
        priority=ticket_data.priority.value if ticket_data.priority else "Medium"
    )
 
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
 
    return TicketCreateResponse(
        ticket_id=new_ticket.ticket_id,
        created_at=new_ticket.created_at
    )