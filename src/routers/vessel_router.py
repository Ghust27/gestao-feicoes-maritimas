from fastapi import APIRouter, HTTPException, status, Depends
from src.services.vessel import VesselService
from src.schemas.vessel import VesselDTO, VesselUpdateDTO
from uuid import UUID


router = APIRouter(prefix="/vessels", tags=["vessels"])

@router.get("/", status_code=status.HTTP_200_OK)
def get_vessels(service: VesselService = Depends(get_vessel_service)):
    vessels = service.get_all()
    return vessels
    

@router.get("/{vessel_id}", status_code=status.HTTP_200_OK)
def get_vessel_by_id(vessel_id: UUID, service: VesselService = Depends(get_vessel_service)):
    try:
        vessel = service.get_by_id(vessel_id)
        return vessel
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vessel(data: VesselDTO, service: VesselService = Depends(get_vessel_service)):
    try:
        new_vessel = service.create(data=data)
        return new_vessel
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )

@router.patch("/[{mmsi}]", status_code=status.HTTP_200_OK)
def update_vessel(mmsi: str, data: VesselUpdateDTO, service: VesselService = Depends(get_vessel_service)):
    try:
        vessel = service.update(data=data)
        return vessel
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
            )
    
@router.delete("/{mmsi}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vessel(vessel_id: UUID, service: VesselService = Depends(get_vessel_service)):
    try:
        vessel = service.delete(vessel_id=vessel_id)
        return 
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )