import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas import AddressCreate, AddressUpdate, NearbyQuery
from app.models import Address
from geopy.distance import geodesic

logger = logging.getLogger(__name__)

def get_adresses(db: Session, skip: int = 0, pageSize: int = 10) -> List[Address]:
    """_summary_
        returns a paginated list of addresses
    Args:
        db (Session): db session instance
        skip (int, optional): page offset. Defaults to 0.
        pageSize (int, optional): how many addresses to display. Defaults to 10.

    Returns:
        List[Address]: filtered address list
    """
    res = db.query(Address).offset(skip).limit(pageSize).all()
    logger.info(f"Returned %{len(res)} addresses")
    return res

def get_address(db: Session, id: int) -> Optional[Address]:
    """returns a specific address based on ID

    Args:
        db (Session): db session instance
        id (int): ID number of Address we want to find

    Returns:
        Address: Address object found
    """
    address = db.query(Address).filter(Address.id == id).first()
    if address is None:
        logger.warning("Address does not exist")
        return None
    
    logger.info(f"Found Address ID %{address.id}")
        
    return address

def create_address(db: Session, data: AddressCreate) -> Address:
    """creates new address from form data

    Args:
        db (Session): db session instance
        data (AddressCreate): validated form data

    Returns:
        Address: newly created address
    """
    address = Address(**data.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    logger.info(f"Created new address ID %{address.id}")
    return address

def update_address(db: Session, id: int, data: AddressUpdate) -> Optional[Address]:
    """Updates attribute/s of Address with ID

    Args:
        db (Session): db session instance
        id (int): ID number of Address we want to modify 
        data (AddressUpdate): edit data

    Returns:
        Optional[Address]: returns Address or None
    """
    address = get_address(db, id)
    if address is None:
        logger.warning("Update failed")
        return None

    updated = data.model_dump(exclude_unset=True)
    for field, value in updated.items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    logger.info(f"Updated Addres ID %{id} fields=%{list(updated.keys())}")
    return address

def delete_address(db: Session, id: int) -> bool:
    """delete an address based on id number

    Args:
        db (Session): db session instance
        id (int): ID number of Address we want to delete
    
    Returns:
        bool: boolean that determines whether delete is successful
    """
    address = get_address(db, id)
    
    if address is None:
        logger.warning("Delete failed")
        return False
    
    db.delete(address)
    db.commit()
    logger.info(f"Delete Address ID %{id} successful")
    return True

def get_nearby_addresses( db: Session, data: NearbyQuery) -> List[Address]:
    """ Return all addresses within given distance using Geopy library

    Args:
        db (Session): db session instance
        latitude (float): latitude of reference address
        longitude (float): latitude of reference address
        distance (float): search radius

    Returns:
        List[Addresses]: addresses found within distance
    """
    center = (data.latitude, data.longitude)
    all_addresses = db.query(Address).all()
    nearby = [
        a for a in all_addresses
        if geodesic(center, (a.latitude, a.longitude)).km <= data.distance
    ]
    
    logger.info(f"Found {len(nearby)} address/es within %{data.distance} km radius")
    
    return nearby