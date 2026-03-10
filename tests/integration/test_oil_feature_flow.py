"""
Integration test: full flow per requirements.
Create feature, associate with two vessels, confirm and validate final state.

Requires PostgreSQL running (e.g. docker compose up -d db).
Set DB_URL in .env or environment variable.
"""
import os
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

os.environ.setdefault("ALGORITHM", "HS256")

# Integration test requires PostgreSQL - SQLite does not support native UUID
_db_url = os.getenv("DB_URL")
if not _db_url or "sqlite" in _db_url:
    pytest.skip(
        "Integration test requires PostgreSQL. Set DB_URL (e.g. postgresql://user:pass@localhost/db)",
        allow_module_level=True,
    )

from src.api.main import app
from src.core.database import SessionLocal
from src.infrastructure.database.models.oil_feature import oil_feature_vessels


@pytest.fixture
def client():
    """Test client."""
    return TestClient(app)


def _create_user_and_login(client: TestClient, role: str):
    email = f"{role}.{uuid4().hex[:8]}@test.com"
    create_resp = client.post(
        "/users/",
        json={
            "name": f"{role.title()} Test",
            "email": email,
            "password": "admin123",
            "role": role,
        },
    )
    assert create_resp.status_code == 201, create_resp.text

    resp = client.post(
        "/auth/login",
        json={"email": email, "password": "admin123"},
    )
    assert resp.status_code == 200
    return {
        "token": resp.json()["access_token"],
        "id": create_resp.json()["id"],
        "email": email,
    }


@pytest.fixture
def admin_token(client):
    """Create admin user and return JWT token."""
    return _create_user_and_login(client, role="admin")["token"]


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_full_oil_feature_flow(client, admin_token):
    """
    Full flow: create feature, associate with two vessels,
    confirm and validate final state.
    """
    headers = _auth_headers(admin_token)
    mmsi_1 = uuid4().int % 900000000 + 100000000
    mmsi_2 = uuid4().int % 900000000 + 100000000
    mmsi_1 = str(mmsi_1)
    mmsi_2 = str(mmsi_2)

    # 1. Create two vessels
    v1 = client.post(
        "/vessels/",
        json={
            "mmsi": mmsi_1,
            "name": "Vessel One",
            "vessel_type": "osv",
            "active": True,
        },
        headers=headers,
    )
    assert v1.status_code == 201, v1.text

    v2 = client.post(
        "/vessels/",
        json={
            "mmsi": mmsi_2,
            "name": "Vessel Two",
            "vessel_type": "ahts",
            "active": True,
        },
        headers=headers,
    )
    assert v2.status_code == 201, v2.text

    # 2. Create oil feature
    feat = client.post(
        "/oil-features/",
        json={
            "latitude": -22.5,
            "longitude": -43.2,
            "estimated_area": 100.5,
            "confidence_level": 85,
        },
        headers=headers,
    )
    assert feat.status_code == 201, feat.text
    feature_id = feat.json()["id"]

    # 3. Associate feature with both vessels
    assoc1 = client.post(
        f"/oil-features/{feature_id}/vessels/{mmsi_1}",
        headers=headers,
    )
    assert assoc1.status_code == 200, assoc1.text

    assoc2 = client.post(
        f"/oil-features/{feature_id}/vessels/{mmsi_2}",
        headers=headers,
    )
    assert assoc2.status_code == 200, assoc2.text

    # Validate feature is associated to exactly two vessels in the association table.
    db = SessionLocal()
    try:
        associated_count = db.execute(
            select(func.count())
            .select_from(oil_feature_vessels)
            .where(oil_feature_vessels.c.oil_feature_id == UUID(feature_id))
        ).scalar_one()
        assert associated_count == 2
    finally:
        db.close()

    # 4. Confirm feature
    confirm = client.patch(
        f"/oil-features/{feature_id}/confirm",
        headers=headers,
    )
    assert confirm.status_code == 200, confirm.text

    # 5. Validate final state
    get_feat = client.get(f"/oil-features/{feature_id}", headers=headers)
    assert get_feat.status_code == 200, get_feat.text
    data = get_feat.json()

    assert data["status"] == "CONFIRMED"
    assert data["confirmed_by"] is not None
    assert data["confirmation_date"] is not None
    assert data["latitude"] == -22.5
    assert data["longitude"] == -43.2
    assert data["confidence_level"] == 85
    assert data["estimated_area"] == 100.5


def test_operator_cannot_discard_oil_feature(client):
    operator = _create_user_and_login(client, role="operator")
    headers = _auth_headers(operator["token"])

    feat = client.post(
        "/oil-features/",
        json={
            "latitude": -10.0,
            "longitude": -20.0,
            "estimated_area": 50.0,
            "confidence_level": 70,
        },
        headers=headers,
    )
    assert feat.status_code == 201, feat.text
    feature_id = feat.json()["id"]

    discard = client.patch(f"/oil-features/{feature_id}/discard", headers=headers)
    assert discard.status_code == 403, discard.text
    assert discard.json()["detail"] == "Access denied."


def test_cannot_update_confirmed_oil_feature(client, admin_token):
    headers = _auth_headers(admin_token)

    feat = client.post(
        "/oil-features/",
        json={
            "latitude": -21.0,
            "longitude": -42.0,
            "estimated_area": 75.0,
            "confidence_level": 88,
        },
        headers=headers,
    )
    assert feat.status_code == 201, feat.text
    feature_id = feat.json()["id"]

    confirm = client.patch(f"/oil-features/{feature_id}/confirm", headers=headers)
    assert confirm.status_code == 200, confirm.text

    patch_resp = client.patch(
        f"/oil-features/{feature_id}",
        json={"estimated_area": 10.0},
        headers=headers,
    )
    assert patch_resp.status_code == 404, patch_resp.text
    assert patch_resp.json()["detail"] == "Cannot update a confirmed or discarded feature."


def test_cannot_associate_inactive_vessel(client, admin_token):
    headers = _auth_headers(admin_token)
    mmsi = str(uuid4().int % 900000000 + 100000000)

    vessel = client.post(
        "/vessels/",
        json={
            "mmsi": mmsi,
            "name": "Inactive Vessel",
            "vessel_type": "osv",
            "active": True,
        },
        headers=headers,
    )
    assert vessel.status_code == 201, vessel.text

    updated = client.put(
        f"/vessels/{mmsi}",
        json={"active": False},
        headers=headers,
    )
    assert updated.status_code == 200, updated.text

    feat = client.post(
        "/oil-features/",
        json={
            "latitude": -15.0,
            "longitude": -39.0,
            "estimated_area": 90.0,
            "confidence_level": 64,
        },
        headers=headers,
    )
    assert feat.status_code == 201, feat.text
    feature_id = feat.json()["id"]

    assoc = client.post(f"/oil-features/{feature_id}/vessels/{mmsi}", headers=headers)
    assert assoc.status_code == 400, assoc.text
    assert assoc.json()["detail"] == "Cannot associate oil feature with inactive vessel."


def test_cannot_confirm_discarded_oil_feature(client, admin_token):
    headers = _auth_headers(admin_token)

    feat = client.post(
        "/oil-features/",
        json={
            "latitude": -19.0,
            "longitude": -40.0,
            "estimated_area": 80.0,
            "confidence_level": 60,
        },
        headers=headers,
    )
    assert feat.status_code == 201, feat.text
    feature_id = feat.json()["id"]

    discard = client.patch(f"/oil-features/{feature_id}/discard", headers=headers)
    assert discard.status_code == 200, discard.text

    confirm = client.patch(f"/oil-features/{feature_id}/confirm", headers=headers)
    assert confirm.status_code == 400, confirm.text
    assert confirm.json()["detail"] == "Cannot confirm a discarded oil feature."


def test_cannot_delete_user_with_confirmed_feature(client, admin_token):
    admin_headers = _auth_headers(admin_token)
    operator = _create_user_and_login(client, role="operator")
    operator_headers = _auth_headers(operator["token"])

    feat = client.post(
        "/oil-features/",
        json={
            "latitude": -18.0,
            "longitude": -41.0,
            "estimated_area": 66.0,
            "confidence_level": 77,
        },
        headers=operator_headers,
    )
    assert feat.status_code == 201, feat.text
    feature_id = feat.json()["id"]

    confirm = client.patch(f"/oil-features/{feature_id}/confirm", headers=operator_headers)
    assert confirm.status_code == 200, confirm.text

    delete_resp = client.delete(f"/users/{operator['id']}", headers=admin_headers)
    assert delete_resp.status_code == 404, delete_resp.text
    assert delete_resp.json()["detail"] == "Cannot delete a user with confirmed features."
