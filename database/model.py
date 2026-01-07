from sqlalchemy import Column, Integer, String, Enum
from database.database import Base,engine

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(50), nullable=False)
    phone_no = Column(String(10), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True) # address = lat long (frontend)

class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String(40), nullable=False)
    tiffin_center_name = Column(String(100), nullable=True)
    tiffin_category = Column(Enum("veg", "non veg", name="tiffin_category"),nullable=True)
    phone_no = Column(String(10), unique=True, nullable=False)
    alternative_phone_no = Column(String(10), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    # address from frontend in latitude longitude
    address = Column(String(255), nullable=True) 
    # class address (street_no & area, city , pincode) :- its just a suggestion
    city = Column(String(50), nullable=True)
    pincode = Column(String(10), nullable=True)

# This create tables in the database
Base.metadata.create_all(bind=engine)