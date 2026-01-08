from sqlalchemy.orm import Session #Session = Database ke saath baat karne ka medium (query, commands- data insert/update/delete nahi kar sakte, transaction manage nahi hota)
from database.model import Customer, Vendor
from Auth.auth_dto import (
    UserRole,
    SignupDTO,
    LoginDTO,
    GetProfileDTO,
    UpdateProfileDTO
)
from utils.auth_utils import hash_password, verify_password


class AuthService:

    @staticmethod
    def signup_user(db: Session, payload: SignupDTO):

        # Password confirmation here your password must eaqul to confirm password
        if payload.password != payload.confirm_password:
            raise ValueError("Passwords do not match")
        
        # Global phone check from both tables customers and vendors 
        # hum yaha par phone number and otp login karewnge thats why phone ka constrain add kiya h 
        phone_exists = (
            db.query(Customer).filter(Customer.phone_no == payload.phone_no).first()
            or
            db.query(Vendor).filter(Vendor.phone_no == payload.phone_no).first()
        )

        if phone_exists:
            raise ValueError("Phone number already registered")

        hashed_password = hash_password(payload.password) #payload k password ko hash kar diya

        # customer(user role h) SIGNUP 
        if payload.category_type == UserRole.customer:

            # phone unique check
            #if db.query(Customer).filter(
             #   Customer.contact_no == payload.phone_no
            #).first():
            #    raise ValueError("Phone number already registered")

            customer = Customer(
                customer_name=payload.name,
                phone_no=payload.phone_no,
                email=payload.email,
                password_hash=hashed_password
            )

            db.add(customer)
            db.commit()
            db.refresh(customer)

            return {
                "user_id": customer.customer_id
            }

        #VENDOR SIGNUP
        if payload.category_type == UserRole.vendor:

            # phone unique check
            #if db.query(Vendor).filter(
                #Vendor.contact_no == #payload.phone_no
            #).first():
                #raise ValueError("Phone number already registered")

            vendor = Vendor(
                vendor_name=payload.name,
                phone_no=payload.phone_no,
                email=payload.email,
                password_hash=hashed_password
            )

            db.add(vendor)
            db.commit()
            db.refresh(vendor)

            return {
                "user_id": vendor.vendor_id
            }

        # if the user have wrong category then the signup will through not valid category error 
        raise ValueError("Invalid category type")

    
    @staticmethod
    def login_user(db: Session, payload: LoginDTO):

    # CUSTOMER LOGIN
        if payload.category_type == UserRole.customer:
            customer = db.query(Customer).filter(
            Customer.phone_no == payload.phone_no
        ).first()

            if not customer:
                raise ValueError("Phone number not registered")

            if not verify_password(payload.password, customer.password_hash):
                raise ValueError("Invalid password")

            return {
            "message": "Login successful",
            "user_type": "customer",
            "user_id": customer.customer_id
            }

    #  VENDOR LOGIN
        elif payload.category_type == UserRole.vendor:
            vendor = db.query(Vendor).filter(
            Vendor.phone_no == payload.phone_no
        ).first()

            if not vendor:
                raise ValueError("Phone number not registered")

            if not verify_password(payload.password, vendor.password_hash):
                raise ValueError("Invalid password")

            return {
            "message": "Login successful",
            "user_type": "vendor",
            "user_id": vendor.vendor_id
            }

        else:
            raise ValueError("Invalid user role")
   
    @staticmethod
    def get_profile(db: Session, payload: GetProfileDTO):

    # CUSTOMER PROFILE
        if payload.category_type == UserRole.customer:
            user = db.query(Customer).filter(
            Customer.contact_no == payload.phone_no
            ).first()

            if not user:
                raise ValueError("Customer not found")

            if not verify_password(payload.password, user.password_hash):
                raise ValueError("Invalid password")

            return user

    # VENDOR PROFILE
        elif payload.category_type == UserRole.vendor:
            user = db.query(Vendor).filter(
            Vendor.contact_no == payload.phone_no
            ).first()

            if not user:
                raise ValueError("Vendor not found")

            if not verify_password(payload.password, user.password_hash):
                raise ValueError("Invalid password")

            return user

        else:
            raise ValueError("Invalid user role")

    
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
