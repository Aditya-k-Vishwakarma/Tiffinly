from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
from enum import Enum

class UserRole(str, Enum):
    customer = "customer"
    vendor = "vendor"

class SignupDTO(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone_no: Annotated[str, Field(..., pattern=r"^[6-9]\d{9}$")]
    category_type: UserRole = Field(...)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=8)
    confirm_password : str = Field(...)
    # address add karna h frontend se lat long m

class LoginDTO(BaseModel):
    #email: Optional[EmailStr] = None 
    # suggestion by chnages agar phone nhi hua toh email se bhi long ho jaye suggestion
    phone_no : Annotated[str, Field(...,pattern=r"^[6-9]\d{9}$")]
    password: str = Field(..., min_length=8) 
    #forget password? kese hoga? like otp on same registered number and then confirm and then update password
    category_type: UserRole = Field(...) 
    #particular table search k liye 

class GetProfileDTO(BaseModel):
    user_id: int= Field(...)
    category_type: UserRole = Field(...)
    
class CustomerUpdateProfileDTO(BaseModel):
    customer_id: int
    customer_name: Optional[str] = None
    address: Optional[str] = None

class VendorUpdateProfileDTO(BaseModel):
    vendor_id : int
    vendor_name: Optional[str] = None
    tiffin_center_name: Optional[str] = None
    tiffin_category: Optional[str] = None
    #alternative_phone_no : Optional[int] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None


class DeleteProfileDTO(BaseModel):
    phone_no: Annotated[str, Field(..., pattern=r"^[6-9]\d{9}$")]
    password: str = Field(..., min_length=8)
    category_type: UserRole = Field(...)



class BaseUserResponseDTO(BaseModel):
    user_id: int
    phone_no: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None

    model_config = {"from_attributes": True}

class CustomerResponseDTO(BaseUserResponseDTO):
    customer_name: str
    category_type: str = "customer"

class VendorResponseDTO(BaseUserResponseDTO):
    vendor_name: str
    tiffin_center_name: Optional[str] = None
    tiffin_category: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None

    category_type: str = "vendor"
