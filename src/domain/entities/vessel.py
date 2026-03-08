""" Embarcação: mmsi (PK, 9 dígitos numéricos), nome, imo (único opcional), tipo, ativo (bool),
created_at. Não permitir exclusão se houver vínculo com feições. """

from datetime import datetime,timezone
from src.schemas.vessel import VesselDTO

class Vessel:
    def __init__(
            self, data: VesselDTO, 
            active: bool=True, create_at: datetime = None
    ):
        self.mmsi = data.mmsi 
        self.name = data.name
        self.type = data.vessel_type 
        self.active = data.active 
        self.create_at = create_at or datetime.now(timezone.utc)
        self.imo = data.imo 

    def validate_delete(self, associated_features: int):
        if associated_features > 0:
            raise ValueError("Cannot delete a vessel with associated features.")
        
        return True