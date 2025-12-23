from sqlalchemy.orm import Session
from database.model import User
from Auth.auth_dto import (
    SignupDTO,
    LoginDTO,
    GetProfileDTO,
    UpdateProfileDTO
)
from utils.auth_utils import hash_password, verify_password


class AuthService:

    # ================= SIGNUP =================
    @staticmethod
    def signup_user(db: Session, payload: SignupDTO):
        if db.query(User).filter(User.email == payload.email).first():
            raise ValueError("Email already registered")

        user = User(
            username=payload.name,
            email=payload.email,
            password_hash=hash_password(payload.password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ✅ user_id return for verification
        return {"user_id": user.user_id}


    # ================= LOGIN =================
    @staticmethod
    def login_user(db: Session, payload: LoginDTO):
        user = db.query(User).filter(User.email == payload.email).first()

        if not user or not verify_password(payload.password, user.password_hash):
            raise ValueError("Invalid email or password")

        return {"message": "Login successful"}


    # ================= GET PROFILE =================
    @staticmethod
    def get_profile(db: Session, payload: GetProfileDTO):
        user = db.query(User).filter(User.email == payload.email).first()

        if not user or not verify_password(payload.password, user.password_hash):
            raise ValueError("Invalid email or password")

        return user


    # ================= UPDATE PROFILE =================
    @staticmethod
    def update_profile(db: Session, payload: UpdateProfileDTO):
        user = db.query(User).filter(User.user_id == payload.user_id).first()

        if not user:
            raise ValueError("User not found")

        # Empty value → old value remains
        if payload.name not in (None, ""):
            user.username = payload.name

        if payload.contact_no not in (None, ""):
            user.contact_no = payload.contact_no

        if payload.category_type not in (None, ""):
            user.category_type = payload.category_type

        if payload.address not in (None, ""):
            user.address = payload.address

        db.commit()
        db.refresh(user)

        return user


    # ================= DELETE PROFILE =================
    @staticmethod
    def delete_profile(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise ValueError("Invalid email")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid password")

        db.delete(user)
        db.commit()

        return {"message": "User deleted successfully"}
