from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app=FastAPI()
class Customer(BaseModel):
  customer_name: str
  customer_email: EmailStr
  cusomer_Age: int
  
@app.post("/create_customer")
def create_customer(customer: Customer):
  return customer