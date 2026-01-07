from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
from enum import Enum

class UserRole(str, Enum):
    customer = "customer"
    vendor = "vendor"

class SignupDTO(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone_no: Annotated[str, Field(pattern=r"^[6-9]\d{9}$")]
    category_type: UserRole = Field(...)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8)
    confirm_password : str = Field(...)
    # address add karna h frontend se lat long m

class LoginDTO(BaseModel):
    email: Optional[EmailStr] = None 
    #by chnages agar phone nhi hua toh email se bhi long ho jaye suggestion
    phone_no : Annotated[str, Field(...,pattern=r"^[6-9]\d{9}$")]
    password: str = Field(..., min_length=8) 
    #forget password? kese hoga? like otp on same registered number and then confirm and then update password
    category_type: UserRole = Field(...) 
    #particular table search k liye 

class GetProfileDTO(BaseModel):
    phone_no : Annotated[str, Field(...,pattern=r"^[6-9]\d{9}$")] 
    #yaha par alternative contact no k sath bhi password ki linking hga uske sath bhi login hoga? 
    password: str = Field(..., min_length=8)
    category_type: UserRole = Field(...)


class UpdateProfileDTO(BaseModel):
    user_id: int
    name: Optional[str] = None
    contact_no: Optional[str] = None
    category_type: Optional[str] = None
    address: Optional[str] = None


class DeleteProfileDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserResponseDTO(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    contact_no: Optional[str] = None
    category_type: Optional[str] = None
    address: Optional[str] = None

    model_config = {"from_attributes": True}
