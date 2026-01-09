from sqlalchemy.orm import Session #Session = Database ke saath baat karne ka medium (query, commands- data insert/update/delete nahi kar sakte, transaction manage nahi hota)
from database.model import Customer, Vendor
from Auth.auth_dto import (
    UserRole,
    SignupDTO,
    LoginDTO,
    GetProfileDTO,
    CustomerUpdateProfileDTO,
    VendorUpdateProfileDTO,
    DeleteProfileDTO,
    CustomerResponseDTO,
    VendorResponseDTO
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

        if payload.category_type == UserRole.customer:
            user = db.query(Customer).filter(
                Customer.customer_id == payload.user_id
            ).first()

            if not user:
                raise ValueError("Customer not found")

            return {
                "user_id": user.customer_id,
                "phone_no": user.phone_no,
                "email": user.email,
                "address": user.address,
                "customer_name": user.customer_name,
                "category_type": "customer"
            }

        elif payload.category_type == UserRole.vendor:
            user = db.query(Vendor).filter(
                Vendor.vendor_id == payload.user_id
            ).first()

            if not user:
                raise ValueError("Vendor not found")

            return {
                "user_id": user.vendor_id,
                "phone_no": user.phone_no,
                "email": user.email,
                "address": user.address,
                "vendor_name": user.vendor_name,
                "tiffin_center_name": user.tiffin_center_name,
                "tiffin_category": user.tiffin_category,
                "city": user.city,
                "pincode": user.pincode,
                "category_type": "vendor"
            }

        else:
            raise ValueError("Invalid user role")

    
    @staticmethod
    def update_customer_profile(db: Session, payload: CustomerUpdateProfileDTO):

        customer = db.query(Customer).filter(
            Customer.customer_id == payload.customer_id
        ).first()

        if not customer:
            raise ValueError("Customer not found")

        if payload.customer_name not in (None, ""):
            customer.customer_name = payload.customer_name

        if payload.address not in (None, ""):
            customer.address = payload.address

        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def update_vendor_profile(db: Session, payload: VendorUpdateProfileDTO):

        vendor = db.query(Vendor).filter(
            Vendor.vendor_id == payload.vendor_id
        ).first()

        if not vendor:
            raise ValueError("Vendor not found")

        if payload.vendor_name not in (None, ""):
            vendor.vendor_name = payload.vendor_name

        if payload.tiffin_center_name not in (None, ""):
            vendor.tiffin_center_name = payload.tiffin_center_name

        if payload.tiffin_category not in (None, ""):
            vendor.tiffin_category = payload.tiffin_category

        #if payload.alternative_phone_no not in (None, ""):
            #vendor.alternative_phone_no = payload.alternative_phone_no

        if payload.address not in (None, ""):
            vendor.address = payload.address

        if payload.city not in (None, ""):
            vendor.city = payload.city

        if payload.pincode not in (None, ""):
            vendor.pincode = payload.pincode

        db.commit()
        db.refresh(vendor)

        return vendor

    @staticmethod
    def delete_profile(db: Session, payload: DeleteProfileDTO):
        """
        Delete customer or vendor profile using phone_no + password
        """

        # -------- CUSTOMER --------
        if payload.category_type == UserRole.customer:
            user = db.query(Customer).filter(
                Customer.phone_no == payload.phone_no
            ).first()

            if not user:
                raise ValueError("Customer not found")

            if not verify_password(payload.password, user.password_hash):
                raise ValueError("Incorrect password")

            db.delete(user)
            db.commit()
            return {"message": "Customer profile deleted successfully"}

        # -------- VENDOR --------
        elif payload.category_type == UserRole.vendor:
            user = db.query(Vendor).filter(
                Vendor.phone_no == payload.phone_no
            ).first()

            if not user:
                raise ValueError("Vendor not found")

            if not verify_password(payload.password, user.password_hash):
                raise ValueError("Incorrect password")

            db.delete(user)
            db.commit()
            return {"message": "Vendor profile deleted successfully"}

        # -------- INVALID ROLE --------
        else:
            raise ValueError("Invalid category_type")
