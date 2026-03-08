import pytest
from src.domain.entities.oil_feature import OilFeature
from src.schemas.oil_feature import OilFeatureDTO
from uuid import UUID,uuid4
from datetime import datetime, timezone

@pytest.fixture
def base_oil_feature():
    return OilFeatureDTO(
        latitude=10,
        longitude=12,
        estimated_area=25,
        confidence_level=45,
        status="detected"
    )

def test_generation_of_uuid_and_detection_date(base_oil_feature):
    oil_feature = OilFeature(
        base_oil_feature
        )

    assert isinstance(oil_feature.id, UUID)
    assert oil_feature.detection_date is not None
    assert oil_feature.confirmed_by is None
    assert oil_feature.confirmation_date is None


def test_oil_feature_must_respect_provided_id_and_date(base_oil_feature):
    expected_id = uuid4()
    expected_oil_feature_detection_date = datetime(2026,3,5,tzinfo=timezone.utc)
    oil_feature = OilFeature(
        base_oil_feature,
        id=id,
        detection_date=expected_oil_feature_detection_date
        )
    
    assert oil_feature.id == id
    assert oil_feature.detection_date == expected_oil_feature_detection_date
