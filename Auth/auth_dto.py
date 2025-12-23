from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class SignupDTO(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class LoginDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class GetProfileDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


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
