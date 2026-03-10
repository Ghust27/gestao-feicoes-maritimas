from typing import List
from sqlalchemy.orm import Session
from src.infrastructure.database.models.vessel import VesselModel
from src.domain.entities.vessel import Vessel
from src.schemas.vessel import VesselDTO, VesselUpdateDTO, VesselTypes


def _model_to_vessel(model: VesselModel) -> Vessel:
    vessel_type = (
        VesselTypes(model.vessel_type)
        if isinstance(model.vessel_type, str)
        else model.vessel_type
    )
    dto = VesselDTO(
        mmsi=model.mmsi,
        name=model.name,
        vessel_type=vessel_type,
        imo=model.imo,
        active=model.active,
    )
    return Vessel(data=dto, create_at=model.created_at)


class VesselRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Vessel]:
        models = self.db.query(VesselModel).all()
        return [_model_to_vessel(m) for m in models]

    def get_by_id(self, mmsi: str) -> Vessel | None:
        model = self.db.query(VesselModel).filter(VesselModel.mmsi == mmsi).first()
        return _model_to_vessel(model) if model else None

    def create_vessel(self, vessel: Vessel) -> Vessel:
        model = VesselModel(
            mmsi=vessel.mmsi,
            name=vessel.name,
            imo=vessel.imo,
            vessel_type=vessel.type.value if hasattr(vessel.type, "value") else str(vessel.type),
            active=vessel.active,
            created_at=vessel.create_at,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _model_to_vessel(model)

    def get_associated_oil_features(self, vessel_mmsi: str) -> int:
        model = self.db.query(VesselModel).filter(VesselModel.mmsi == vessel_mmsi).first()
        if not model:
            return 0
        return len(model.oil_features)

    def update_vessel(self, vessel_mmsi: str, data: VesselUpdateDTO) -> Vessel | None:
        model = self.db.query(VesselModel).filter(VesselModel.mmsi == vessel_mmsi).first()
        if not model:
            return None
        update_dict = data.model_dump(exclude_unset=True)
        if "vessel_type" in update_dict and update_dict["vessel_type"] is not None:
            update_dict["vessel_type"] = (
                update_dict["vessel_type"].value
                if hasattr(update_dict["vessel_type"], "value")
                else update_dict["vessel_type"]
            )
        for key, value in update_dict.items():
            if hasattr(model, key):
                setattr(model, key, value)
        self.db.commit()
        self.db.refresh(model)
        return _model_to_vessel(model)

    def delete_vessel(self, vessel_mmsi: str) -> bool:
        model = self.db.query(VesselModel).filter(VesselModel.mmsi == vessel_mmsi).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False