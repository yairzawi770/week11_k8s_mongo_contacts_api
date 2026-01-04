from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import data_interactor

app = FastAPI()


class Contact(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with Docker!"}

@app.get("/contacts")
def get_contacts():
    return data_interactor.get_all_contacts()


@app.post("/contacts")
def create_contact(contact: Contact):
    contact_id = data_interactor.create_contact(contact)
    return {
        "message": "Contact created successfully",
        "id": contact_id
    }


@app.put("/contacts/{contact_id}")
def update_contact(contact_id: str, contact: Contact):
    success = data_interactor.update_contact(contact_id, contact)
    if not success:
        return "Contact not found"
    return {"message": "Contact updated successfully"}


@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: str):
    success = data_interactor.delete_contact(contact_id)
    if not success:
        return "Contact not found"
    return {"message": "Contact deleted successfully"}