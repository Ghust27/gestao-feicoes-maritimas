from fastapi import APIRouter, HTTPException, status, Depends
from src.services.vessel import VesselService
from src.schemas.vessel import VesselDTO, VesselUpdateDTO
from uuid import UUID
from src.api.dependencies import (
    get_current_user_token,
    require_admin,
    require_operator_or_admin,
    get_vessel_service,
)


router = APIRouter(prefix="/vessels", tags=["vessels"])

@router.get("/", status_code=status.HTTP_200_OK)
def get_vessels(service: VesselService = Depends(get_vessel_service), current_user: dict = Depends(get_current_user_token)):
    vessels = service.get_all()
    return vessels
    

@router.get("/{mmsi}", status_code=status.HTTP_200_OK)
def get_vessel_by_id(mmsi: str, service: VesselService = Depends(get_vessel_service), current_user: dict = Depends(get_current_user_token)):
    try:
        vessel = service.get_by_id(mmsi)
        return vessel
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vessel(data: VesselDTO, service: VesselService = Depends(get_vessel_service), current_user: dict = Depends(require_operator_or_admin)):
    try:
        new_vessel = service.create(data=data)
        return new_vessel
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )

@router.put("/{mmsi}", status_code=status.HTTP_200_OK)
def update_vessel(mmsi: str, data: VesselUpdateDTO, service: VesselService = Depends(get_vessel_service), current_user: dict = Depends(require_operator_or_admin)):
    try:
        vessel = service.update(mmsi=mmsi, data=data)
        return vessel
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
            )
    
@router.delete("/{mmsi}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vessel(mmsi: str, service: VesselService = Depends(get_vessel_service), current_user: dict = Depends(require_admin)):
    try:
        vessel = service.delete(mmsi=mmsi)
        return 
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )