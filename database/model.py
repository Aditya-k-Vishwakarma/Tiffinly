from sqlalchemy import Column, Integer, String
from database.database import Base,engine


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    contact_no = Column(String(15), unique=True, nullable=True)

    password_hash = Column(String(255), nullable=False)

    category_type = Column(String(20), nullable=True)

    address = Column(String(255), nullable=True)


# This line will create tables in the database
Base.metadata.create_all(bind=engine)
