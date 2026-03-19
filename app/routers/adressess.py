import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud
from app.database import get_db
from app.schemas import AddressCreate, AddressResponse, AddressUpdate
from app.models import Address

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/address", tags=["Addresses"])

@router.get("/", response_model=List[AddressResponse])
def get_adresses(skip: int = 0, pageSize: int = 10, db: Session = Depends(get_db)) -> List[AddressResponse]:
    """routes to CRUD get addresses

    Args:
        db (Session): db session instance
        skip (int, optional): page offset. Defaults to 0.
        pageSize (int, optional): how many addresses to display. Defaults to 10.

    Returns:
        List[AddressResponse]: filtered address list
    """
    return crud.get_adresses(db, skip, pageSize)

@router.get("/{id}", response_model=AddressResponse)
def get_address(id: int, db: Session = Depends(get_db)) -> Optional[Address]:
    """routes to CRUD get address

    Args:
        db (Session): db session instance
        id (int): ID number of Address we want to find

    Returns:
        Address: Address object found
    """
    address = crud.get_address(db, id)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return address

@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(payload: AddressCreate, db: Session = Depends(get_db)) -> Address:
    """routes to CRUD create

    Args:
        db (Session): db session instance
        data (AddressCreate): validated form data

    Returns:
        Address: newly created address
    """
    return crud.create_address(db, payload)

@router.put("/{id}", response_model=AddressResponse)
def update_address(payload: AddressUpdate, id: int, db: Session = Depends(get_db)) -> Optional[Address]:
    """route to CRUD update

    Args:
        db (Session): db session instance
        id (int): ID number of Address we want to modify 
        data (AddressUpdate): edit data

    Returns:
        Optional[Address]: returns Address or None
    """
    address = crud.update_address(db, id, payload)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return address

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_address(id: int, db: Session = Depends(get_db)) -> None:
    """routes to CRUD delete address

    Args:
        db (Session): db session instance
        id (int): ID number of Address we want to delete

    """
    if not crud.delete_address(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return None