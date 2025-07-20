from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class Receipt(Base):
    __tablename__ = "receipts"
    id = Column(Integer, primary_key=True, index=True)
    vendor = Column(String, index=True)
    transaction_date = Column(Date)
    amount = Column(Float)
    category = Column(String, nullable=True)
    file_path = Column(String)
