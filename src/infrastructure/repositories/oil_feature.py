from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.infrastructure.database.models.oil_feature import OilFeatureModel
from src.infrastructure.database.models.vessel import VesselModel
from src.domain.entities.oil_feature import OilFeature
from src.schemas.oil_feature import OilFeatureDTO, OilFeatureUpdateDTO, Status

STATUS_MAP = {
    "DETECTED": "DETECTED",
    "CONFIRMED": "CONFIRMED",
    "DISCARDED": "DISCARDED",
    "DETECTADA": "DETECTED",
    "CONFIRMADA": "CONFIRMED",
    "DESCARTADA": "DISCARDED",
}


def _model_to_oil_feature(model: OilFeatureModel) -> OilFeature:
    status_val = STATUS_MAP.get(model.status, model.status)
    status_enum = Status.DETECTED
    if status_val in ("CONFIRMED", "CONFIRMADA"):
        status_enum = Status.CONFIRMED
    elif status_val in ("DISCARDED", "DESCARTADA"):
        status_enum = Status.DISCARDED
    dto = OilFeatureDTO(
        latitude=model.latitude,
        longitude=model.longitude,
        estimated_area=model.estimated_area,
        confidence_level=model.confidence_level,
        status=status_enum,
    )
    return OilFeature(
        data=dto,
        id=model.id,
        detection_date=model.detection_date,
        confirmed_by=str(model.confirmed_by) if model.confirmed_by else None,
        confirmation_date=model.confirmation_date,
    )


class OilFeatureRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_oil_feature(self, oil_feature_id: UUID) -> OilFeature | None:
        model = self.db.query(OilFeatureModel).filter(OilFeatureModel.id == oil_feature_id).first()
        return _model_to_oil_feature(model) if model else None

    def get_all_oil_features(
        self, status: Optional[str] = None, min_confidence_level: Optional[int] = None
    ) -> List[OilFeature]:
        query = self.db.query(OilFeatureModel)
        if status:
            status_db = STATUS_MAP.get(status, status)
            query = query.filter(OilFeatureModel.status == status_db)
        if min_confidence_level is not None:
            query = query.filter(OilFeatureModel.confidence_level >= min_confidence_level)
        return [_model_to_oil_feature(m) for m in query.all()]

    def create_oil_feature(self, oil_feature: OilFeature) -> OilFeature:
        status_db = (
            oil_feature.status.value
            if hasattr(oil_feature.status, "value")
            else STATUS_MAP.get(str(oil_feature.status), "DETECTED")
        )
        status_db = STATUS_MAP.get(status_db, "DETECTED")
        model = OilFeatureModel(
            id=oil_feature.id,
            latitude=oil_feature.latitude,
            longitude=oil_feature.longitude,
            estimated_area=oil_feature.estimated_area,
            confidence_level=oil_feature.confidence_level,
            status=status_db,
            detection_date=oil_feature.detection_date,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _model_to_oil_feature(model)

    def update_oil_feature(
        self, oil_feature_id: UUID, data: OilFeatureUpdateDTO
    ) -> OilFeature | None:
        model = self.db.query(OilFeatureModel).filter(OilFeatureModel.id == oil_feature_id).first()
        if not model:
            return None
        update_dict = data.model_dump(exclude_unset=True)
        if "status" in update_dict and update_dict["status"] is not None:
            status_val = (
                update_dict["status"].value
                if hasattr(update_dict["status"], "value")
                else update_dict["status"]
            )
            update_dict["status"] = STATUS_MAP.get(status_val, "DETECTED")
        for key, value in update_dict.items():
            if hasattr(model, key):
                setattr(model, key, value)
        self.db.commit()
        self.db.refresh(model)
        return _model_to_oil_feature(model)

    def delete_oil_feature(self, oil_feature_id: UUID) -> bool:
        model = self.db.query(OilFeatureModel).filter(OilFeatureModel.id == oil_feature_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False

    def associate_oil_feature_with_vessel(
        self, oil_feature_id: UUID, vessel_mmsi: str
    ) -> bool:
        feature = self.db.query(OilFeatureModel).filter(OilFeatureModel.id == oil_feature_id).first()
        vessel = self.db.query(VesselModel).filter(VesselModel.mmsi == vessel_mmsi).first()
        if not feature or not vessel:
            return False
        if vessel not in feature.vessels:
            feature.vessels.append(vessel)
            self.db.commit()
        return True

    def disassociate_oil_feature_with_vessel(
        self, oil_feature_id: UUID, vessel_mmsi: str
    ) -> bool:
        feature = self.db.query(OilFeatureModel).filter(OilFeatureModel.id == oil_feature_id).first()
        vessel = self.db.query(VesselModel).filter(VesselModel.mmsi == vessel_mmsi).first()
        if not feature or not vessel:
            return False
        if vessel in feature.vessels:
            feature.vessels.remove(vessel)
            self.db.commit()
        return True

    def confirm_oil_feature(self, oil_feature_id: UUID, user_id: UUID) -> OilFeature | None:
        model = self.db.query(OilFeatureModel).filter(OilFeatureModel.id == oil_feature_id).first()
        if not model or model.status == "CONFIRMED":
            return None
        model.status = "CONFIRMED"
        model.confirmed_by = user_id
        model.confirmation_date = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(model)
        return _model_to_oil_feature(model)

    def discard_oil_feature(self, oil_feature_id: UUID) -> OilFeature | None:
        model = self.db.query(OilFeatureModel).filter(OilFeatureModel.id == oil_feature_id).first()
        if not model:
            return None
        model.status = "DISCARDED"
        self.db.commit()
        self.db.refresh(model)
        return _model_to_oil_feature(model)