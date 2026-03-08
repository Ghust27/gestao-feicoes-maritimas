import pytest
from src.domain.entities.vessel import Vessel
from src.schemas.vessel import VesselDTO, VesselTypes


@pytest.fixture
def base_vessel():
    vessel_dto = VesselDTO(
        mmsi="13221321312",
        name="Vessel Test",
        vessel_type=VesselTypes.OSV,
    )
    return Vessel(vessel_dto)

def test_generation_of_creation_date(base_vessel):
    assert base_vessel.create_at is not None

def test_cannot_delete_vessel_with_associated_oil_feature(base_vessel):
    with pytest.raises(ValueError) as err:
        base_vessel.validate_delete(1)
    assert str(err.value) == "Cannot delete a vessel with confirmed features."