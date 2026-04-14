from fastapi import APIRouter, HTTPException
from models.user import BaseResponseModel, AddUser, AddUserResponse
from db import db, to_object_id, serialize_doc, users_collection




user_router = APIRouter()

def validate_password(password: str):
    special_chars = ["!", "@", "£", "$", "%", "^", "&", "*", "(", ")"]

    is_special = False
    for i in password:
        for j in special_chars:
            if i == j:
                is_special = True
    
    if is_special and len(password) >= 8:
        pass
    else: return HTTPException(status_code=406, detail="Password does not meet criteria")
    

    
@user_router.post("/signup", response_model=AddUserResponse)
def add_user(user: AddUser):
    
    user_dict = user.model_dump()

    if user_dict["email"] in users_collection.find_one():
        return HTTPException(status_code=400, detail="Email already exists under different account")
    

    