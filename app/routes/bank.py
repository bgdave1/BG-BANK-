from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import database, models, schemas
from app.utils.auth_utils import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Bank)
def create_bank(
    bank: schemas.BankCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    new_bank = models.Bank(**bank.dict(), owner_id=current_user.id)
    db.add(new_bank)
    db.commit()
    db.refresh(new_bank)
    return new_bank

@router.get("/", response_model=list[schemas.Bank])
def get_banks(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Bank).filter(models.Bank.owner_id == current_user.id).all()

@router.get("/{bank_id}", response_model=schemas.Bank)
def get_bank(
    bank_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    bank = db.query(models.Bank).filter(models.Bank.id == bank_id).first()
    if not bank or bank.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Bank not found or access denied")
    return bank

@router.delete("/{bank_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank(
    bank_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    bank = db.query(models.Bank).filter(models.Bank.id == bank_id).first()
    if not bank or bank.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Bank not found or access denied")
    db.delete(bank)
    db.commit()
    return
