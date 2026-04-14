from fastapi import APIRouter, HTTPException
from models.user import  AddUser, AddUserResponse
from db import db, to_object_id, serialize_doc, users_collection
from security import hash_password

user_router= APIRouter()

def validate_password(password: str):
    special_chars = ["!", "@", "£", "$", "%", "^", "&", "*", "(", ")"]

    is_special = False
    for i in password:
        for j in special_chars:
            if i == j:
                is_special = True
    
    if is_special and len(password) >= 8:
        pass
    else: raise HTTPException(status_code=406, detail="Password does not meet criteria")
    

    
@user_router.post("/signup", response_model=AddUserResponse)
def add_user(user: AddUser):
    
    user_dict = user.model_dump()

    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists under different account")
    

    validate_password(user.password)

    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Password and confirmation password differ")
    else: user_dict.pop("confirm_password", None)


    user_dict["password"] = hash_password(user_dict["password"])

    user_result = users_collection.insert_one(user_dict)

    id = str(user_result.inserted_id)

    return AddUserResponse(status_code=201, msg="Account successfully created", email=user_dict["email"], password=user_dict["password"], account_type=user_dict["account_type"])

