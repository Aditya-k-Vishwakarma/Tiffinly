

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db
from Auth.auth_service import AuthService
from Auth.auth_dto import (
    SignupDTO,
    LoginDTO,
    GetProfileDTO,
    UpdateProfileDTO,
    DeleteProfileDTO,
    UserResponseDTO
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", status_code=201)
def signup(payload: SignupDTO, db: Session = Depends(get_db)):
    try:
        return AuthService.signup_user(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(payload: LoginDTO, db: Session = Depends(get_db)):
    try:
        return AuthService.login_user(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/profile", response_model=UserResponseDTO)
def get_profile(payload: GetProfileDTO, db: Session = Depends(get_db)):
    try:
        return AuthService.get_profile(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


# ================= UPDATE PROFILE =================
@router.put("/profile", response_model=UserResponseDTO)
def update_profile(payload: UpdateProfileDTO, db: Session = Depends(get_db)):
    try:
        return AuthService.update_profile(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/profile")
def delete_profile(payload: DeleteProfileDTO, db: Session = Depends(get_db)):
    try:
        return AuthService.delete_profile(
            db=db,
            email=payload.email,
            password=payload.password
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
