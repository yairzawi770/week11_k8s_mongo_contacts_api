import os
from pymongo import MongoClient
from bson import ObjectId


MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "contactsdb")


client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB]
contacts_collection = db["contacts"]



class Contact:
    def __init__(self, first_name: str, last_name: str, phone_number: str, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
        }

def create_contact(contact) -> str:
    new_contact = {
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "phone_number": contact.phone_number
    }
    result = contacts_collection.insert_one(new_contact)
    return str(result.inserted_id)


def get_all_contacts() -> list:
    contacts_cursor = contacts_collection.find()
    contacts = []
    for row in contacts_cursor:
        contacts.append({
            "id": str(row["_id"]),
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "phone_number": row["phone_number"]
        })
    return contacts


def update_contact(contact_id: str, contact) -> bool:
    try:
        result = contacts_collection.update_one(
            {"_id": ObjectId(contact_id)},  
            {"$set": {
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "phone_number": contact.phone_number
            }}
        )
        return result.matched_count > 0 
    except Exception:
        return False

def delete_contact(contact_id: str) -> bool:
    try:
        result = contacts_collection.delete_one({"_id": ObjectId(contact_id)})
        return result.deleted_count > 0
    except Exception:
        return False