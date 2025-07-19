from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReceiptBase(BaseModel):
    vendor: str
    transaction_date: date
    amount: float
    category: Optional[str] = None

class ReceiptCreate(ReceiptBase):
    pass

class Receipt(ReceiptBase):
    id: int
    file_path: str

    class Config:
        orm_mode = True
