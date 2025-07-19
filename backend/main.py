from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import logging

from . import crud, models, schemas
from .database import SessionLocal, engine
from .parser import parse_receipt

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler = logging.FileHandler('backend.log')
log_handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload/", response_model=schemas.Receipt)
def upload_receipt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed_data = parse_receipt(file_path)
    if not parsed_data:
        raise HTTPException(status_code=400, detail="Could not parse receipt")

    receipt = schemas.ReceiptCreate(**parsed_data)
    return crud.create_receipt(db=db, receipt=receipt, file_path=file_path)

@app.get("/receipts/", response_model=list[schemas.Receipt])
def read_receipts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    receipts = crud.get_receipts(db, skip=skip, limit=limit)
    return receipts

@app.get("/receipts/{receipt_id}", response_model=schemas.Receipt)
def read_receipt(receipt_id: int, db: Session = Depends(get_db)):
    db_receipt = crud.get_receipt(db, receipt_id=receipt_id)
    if db_receipt is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return db_receipt

@app.put("/receipts/{receipt_id}", response_model=schemas.Receipt)
def update_receipt(receipt_id: int, receipt: schemas.ReceiptCreate, db: Session = Depends(get_db)):
    return crud.update_receipt(db=db, receipt_id=receipt_id, receipt=receipt)

@app.delete("/receipts/{receipt_id}", response_model=schemas.Receipt)
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)):
    return crud.delete_receipt(db=db, receipt_id=receipt_id)
