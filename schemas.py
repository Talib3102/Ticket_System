from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum
 

class TicketCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str
    priority: str = "Medium"

class TicketCreateResponse(BaseModel):
    """Minimal response after creating a ticket."""
    ticket_id: str
    created_at: datetime
 
class TicketResponse(BaseModel):
    """Shape of a ticket in list view — no description or notes to keep it fast."""
    id: str
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
 
    class Config:
        from_attributes = True