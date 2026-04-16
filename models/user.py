from pydantic import BaseModel
from typing import Optional, Literal

class BaseResponseModel(BaseModel):
    status_code: int
    msg: str

class AddUser(BaseModel):
    email: str
    password: str
    confirm_password: str
    account_type: Literal["customer", "producer"]

class AddUserResponse(BaseResponseModel):
    email: str
    password: str
    account_type: Literal["customer", "producer"]

class LoginUser(BaseModel):
    email: str
    password: str

class LoginUserResponse(BaseResponseModel):
    id: str
    email: str
    basket: dict


class UpdateUserCustomer:
    email: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None

class Customer(BaseModel):
    _id: str
    email: str
    password: str
    basket: Optional[list] = None

class Producer(BaseModel):
    _id: str
    email: str
    password: str
    basket: list
    full_name: Optional[str] = None
    farming_policy: Optional[str] = None
    production_site_address_1: Optional[str] = None
    production_site_address_2: Optional[str] = None
    production_site_address_3: Optional[str] = None

class Item(BaseModel):
    _id: str
    producer_id: str
    producer_name: str
    price: int
    weight: int # IN GRAMS
    item_name: str
    description: str

class AddItem(BaseModel):
    price: float
    weight: int # IN GRAMS
    item_name: str
    description: str
    image: str
    stock_available: int


class AddItemResponse(BaseResponseModel):
    _id: str
    item_name: str


class UpdateUserProducer(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    full_name: Optional[str] = None
    farming_policy: Optional[str] = None
    production_site_address_1: Optional[str] = None
    production_site_address_2: Optional[str] = None
    production_site_address_3: Optional[str] = None