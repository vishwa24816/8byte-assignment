from sqlalchemy.orm import Session
from . import models, schemas

def get_receipt(db: Session, receipt_id: int):
    return db.query(models.Receipt).filter(models.Receipt.id == receipt_id).first()

def get_receipts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Receipt).offset(skip).limit(limit).all()

def create_receipt(db: Session, receipt: schemas.ReceiptCreate, file_path: str):
    db_receipt = models.Receipt(**receipt.dict(), file_path=file_path)
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt

def update_receipt(db: Session, receipt_id: int, receipt: schemas.ReceiptCreate):
    db_receipt = get_receipt(db, receipt_id)
    if db_receipt:
        for key, value in receipt.dict().items():
            setattr(db_receipt, key, value)
        db.commit()
        db.refresh(db_receipt)
    return db_receipt

def delete_receipt(db: Session, receipt_id: int):
    db_receipt = get_receipt(db, receipt_id)
    if db_receipt:
        db.delete(db_receipt)
        db.commit()
    return db_receipt
