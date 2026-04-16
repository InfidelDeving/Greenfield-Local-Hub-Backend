from bson import ObjectId
from fastapi import HTTPException
from pymongo import MongoClient

#mongodb adress
client = MongoClient("mongodb://localhost:27017")
db = client["database"]
users_collection = db["users"]
items_collection = db["items"]



#MongoDB's id is not stored as a string so we need a quick way of converting from python safe format to a mongo safe format
def to_object_id(id_str: str) -> ObjectId:

    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")


# inverse of the previous function, converts ID from mongo to string and returns a clean document
def serialize_doc_item(doc: dict) -> dict:
    if not doc:
        return doc
    doc["_id"] = str(doc["_id"])
    doc["producer_id"] = str(doc["producer_id"])
    return doc

def serialize_doc_user(doc: dict) -> dict:
    if not doc:
        return doc
    doc["_id"] = str(doc["_id"])
    return doc