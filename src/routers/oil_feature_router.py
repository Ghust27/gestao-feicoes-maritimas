from fastapi import APIRouter, Depends, HTTPException, Query, status
from src.services.oil_feature import OilFeatureService
from src.services.associate_oil_feature import AssociateOilFeatureService
from src.schemas.oil_feature import OilFeatureDTO, OilFeatureUpdateDTO
from src.services.confirm_oil_feature import ConfirmOilFeatureService
from src.services.discard_oil_feature import DiscardOilFeatureService
from typing import Optional
from uuid import UUID
from src.api.dependencies import (
    get_current_user_token,
    require_admin,
    require_operator_or_admin,
    get_oil_feature_service,
    get_associate_oil_feature_service,
    get_confirm_oil_feature_service,
    get_discard_oil_feature_service,
)


router = APIRouter(prefix="/oil-features", tags=["oil features"])

@router.get("/", status_code=status.HTTP_200_OK)
def get_oil_features(
    status_filter: Optional[str] = Query(None, alias="status"),
    min_confidence_level: Optional[int] = Query(None, alias="min_confidence_level"),
    service: OilFeatureService = Depends(get_oil_feature_service),
    current_user: dict = Depends(get_current_user_token),
):
    oil_features = service.get_all(
        status=status_filter, min_confidence_level=min_confidence_level
    )
    return oil_features
    

@router.get("/{oil_feature_id}", status_code=status.HTTP_200_OK)
def get_oil_feature(oil_feature_id: UUID, service: OilFeatureService = Depends(get_oil_feature_service), current_user: dict = Depends(get_current_user_token)):
    try:
        oil_feature = service.get_by_id(oil_feature_id=oil_feature_id)
        return oil_feature
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_oil_feature_(data: OilFeatureDTO, service: OilFeatureService = Depends(get_oil_feature_service), current_user: dict = Depends(require_operator_or_admin)):
    try:
        new_oil_feature_ = service.create(data=data)
        return new_oil_feature_
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )

@router.patch("/{oil_feature_id}", status_code=status.HTTP_200_OK)
def update_oil_feature_(oil_feature_id:UUID, data: OilFeatureUpdateDTO, service: OilFeatureService = Depends(get_oil_feature_service), current_user: dict = Depends(require_operator_or_admin)):
    try:
        oil_feature_ = service.update(oil_feature_id=oil_feature_id, data=data)
        return oil_feature_
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
            )
    
@router.delete("/{oil_feature_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_oil_feature_(oil_feature_id: UUID, service: OilFeatureService = Depends(get_oil_feature_service), current_user: dict = Depends(require_admin)):
    try:
        oil_feature_ = service.delete(oil_feature_id=oil_feature_id)
        return 
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    
@router.post("/{oil_feature_id}/vessels/{mmsi}", status_code=status.HTTP_200_OK)
def associate_vessel_to_feature(oil_feature_id: UUID, mmsi: str, service: AssociateOilFeatureService = Depends(get_associate_oil_feature_service), current_user: dict = Depends(require_admin)):
    try:
        result = service.associate(mmsi= mmsi, oil_feature_id=oil_feature_id)
        return result
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )

@router.delete("/{oil_feature_id}/vessels/{mmsi}", status_code=status.HTTP_204_NO_CONTENT)
def disassociate_vessel_from_feature(
    oil_feature_id: UUID,
    mmsi: str,
    service: AssociateOilFeatureService = Depends(get_associate_oil_feature_service),
    current_user: dict = Depends(require_admin),
):
    try:
        service.disassociate(mmsi=mmsi, oil_feature_id=oil_feature_id)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    
@router.patch("/{oil_feature_id}/confirm", status_code=status.HTTP_200_OK)
def confirm_oil_feature(
    oil_feature_id: UUID,
    service: ConfirmOilFeatureService = Depends(get_confirm_oil_feature_service),
    current_user: dict = Depends(require_operator_or_admin),
):
    try:
        user_id = UUID(current_user["id"])
        result = service.execute(user_id=user_id, oil_feature_id=oil_feature_id)
        return result
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    
@router.patch("/{oil_feature_id}/discard", status_code=status.HTTP_200_OK)
def discard_oil_feature(oil_feature_id: UUID, service: DiscardOilFeatureService = Depends(get_discard_oil_feature_service), current_user: dict = Depends(require_admin)):
    try:
        user_id = UUID(current_user["id"])
        result = service.execute(user_id=user_id, oil_feature_id=oil_feature_id)
        return result
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )