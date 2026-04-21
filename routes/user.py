from fastapi import APIRouter, HTTPException
from models.user import  AddUser, AddUserResponse, LoginUser, LoginUserResponse, Item, AddItem, AddItemResponse, UpdateUserCustomer, UpdateUserProducer, Producer
from db import db, to_object_id, serialize_doc_item, serialize_doc_user, users_collection, items_collection
from security import hash_password, verify_password
from bson import ObjectId

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
    else: raise HTTPException(status_code=406, detail=f"Password must be at least 8 characters long and include one of the following: {special_chars}")
    

    
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
    user_dict["first_login"] = True
    user_result = users_collection.insert_one(user_dict)
    id = str(user_result.inserted_id)
    return AddUserResponse(status_code=201, msg="Account successfully created", email=user_dict["email"], account_type=user_dict["account_type"])


@user_router.post("/login", response_model=LoginUserResponse)
def login_user(details: LoginUser):
    user = users_collection.find_one({"email": details.email})
    if not user or not verify_password(details.password ,user["password"]):
        raise HTTPException(status_code=401, detail="Email or password is incorrect")

    if user["first_login"] == True:
        users_collection.update_one(
            {"email": user["email"]},
            {"$set": {"first_login": False}}
    )


    if "basket" not in user:
        user["basket"] = {}

    return LoginUserResponse(status_code=200, msg="Successfully authenticated", email=user["email"], id=str(user["_id"]), basket=user["basket"], account_type=user["account_type"], first_login=user.get("first_login", False))




@user_router.get("/items")
def get_all_items():

    cursor = items_collection.find()

    items = []
    for doc in cursor:
        serialized = serialize_doc_item(doc)
        items.append(serialized)

    return {"items": items, "lenght": len(items)}


@user_router.get("/itemslimit")
def get_five_items():

    cursor = items_collection.find().limit(5)

    items = []
    for doc in cursor:
        serialized = serialize_doc_item(doc)
        items.append(serialized)

    return {"items": items, "length": len(items)}


@user_router.get("/producers")
def get_all_producers():

    cursor = users_collection.find({"account_type": "producer"})

    producers = []
    for doc in cursor:
        serialized = serialize_doc_user(doc)
        producers.append(serialized)

    return {"producers": producers, "length": len(producers)}


@user_router.get("/producerslimit")
def get_five_producers():

    cursor = users_collection.find({"account_type": "producer"}).limit(5)

    producers = []
    for doc in cursor:
        serialized = serialize_doc_user(doc)
        producers.append(serialized)

    return {"producers": producers, "length": len(producers)}


@user_router.post("/additem", response_model=AddItemResponse)
def add_item(item_details: AddItem, producer_id: str):
    

    producer_dict = users_collection.find_one({"_id": ObjectId(producer_id)})
    if not producer_dict:
        raise HTTPException(status_code=404, detail="Producer not found")
    # validate invalid objectIDs



    new_item_data = item_details.model_dump()
    new_item_data.update({
        "producer_id": producer_dict["_id"],
        "producer_name": producer_dict.get("full_name", "Unknown")
    })

    item_result = items_collection.insert_one(new_item_data)

    return AddItemResponse(
        status_code=200, 
        msg="Item Successfully Added", 
        _id=str(item_result.inserted_id), 
        item_name=item_details.item_name
    )


