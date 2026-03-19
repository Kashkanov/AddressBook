from sqlalchemy import Column, Float, Integer, String
from app.database import Base

class Address(Base):
    __tablename__ = "addressess"
    
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(100), nullable=True)
    houseNo = Column(String(255), nullable=False)
    street = Column(String(255), nullable=False)
    barangay = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)