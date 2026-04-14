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


class UpdateUserProducer:
    email: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    full_name: Optional[str] = None
    farming_policy: Optional[str] = None
    production_site_address_1: Optional[str] = None
    production_site_address_2: Optional[str] = None
    production_site_address_3: Optional[str] = None

    
class UpdateUserCustomer:
    email: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None

class Customer(BaseModel):
    email: str
    password: str
    basket: list

class Producer(BaseModel):
    email: str
    password: str
    basket: list
    full_name: Optional[str] = None
    farming_policy: Optional[str] = None
    production_site_address_1: Optional[str] = None
    production_site_address_2: Optional[str] = None
    production_site_address_3: Optional[str] = None