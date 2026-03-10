# Maritime Feature Management API

A microservice for managing users, vessels, and satellite-detected oil features in offshore monitoring. Operators can validate occurrences and trigger environmental response workflows.

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Domain Model](#domain-model)
- [Business Rules](#business-rules)
- [API Reference](#api-reference)
- [Getting Started](#getting-started)
- [Database & Migrations](#database--migrations)
- [Testing](#testing)
- [Project Structure](#project-structure)

---

## Overview

The platform monitors offshore vessels and possible oil features detected by satellite. It allows operators to:

- Manage **users** (admins and operators)
- Manage **vessels** (ships with MMSI, type, etc.)
- Manage **oil features** (detections with coordinates, confidence, status)
- **Associate** features with vessels
- **Confirm** or **discard** features (with role-based rules)

Authentication is JWT-based; endpoints are protected by role (admin, operator).

---

## Tech Stack

| Component   | Technology        |
|------------|-------------------|
| API        | FastAPI           |
| ORM        | SQLAlchemy 2.x    |
| Migrations | Alembic           |
| Database   | PostgreSQL 15     |
| Auth       | JWT (PyJWT), bcrypt |
| Container  | Docker, Docker Compose |
| Tests      | pytest            |

---

## Architecture

The project follows a layered architecture with clear separation of concerns (SOLID-oriented).

```
┌─────────────────────────────────────────────────────────────────┐
│  API Layer (routers)                                            │
│  HTTP endpoints, request/response, dependency injection          │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  Services (application / use cases)                              │
│  UserService, VesselService, OilFeatureService,                 │
│  AuthService, ConfirmOilFeatureService, DiscardOilFeatureService │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  Domain Layer                                                    │
│  Entities (User, Vessel, OilFeature) + Repository interfaces     │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  Infrastructure                                                  │
│  SQLAlchemy models, repository implementations, database session  │
└─────────────────────────────────────────────────────────────────┘
```

- **API**: FastAPI routers; no business logic, only validation and HTTP handling.
- **Services**: Orchestrate repositories and entities; enforce business rules.
- **Domain**: Entities and repository interfaces (abstractions).
- **Infrastructure**: Concrete repositories and SQLAlchemy models; persistence details.

---

## Domain Model

### User

| Field           | Type   | Description                    |
|----------------|--------|--------------------------------|
| id             | UUID   | Primary key                    |
| name           | string | User name                      |
| email          | string | Unique                         |
| password       | hash   | Stored hashed (bcrypt)        |
| role           | enum   | `admin` or `operator`          |
| active         | bool   | Whether the user can act       |
| created_at     | datetime | Creation timestamp           |

### Vessel

| Field      | Type   | Description                          |
|-----------|--------|--------------------------------------|
| mmsi      | string | Primary key; exactly 9 numeric digits |
| name      | string | Vessel name                          |
| imo       | string | Optional, unique                     |
| vessel_type | string | e.g. osv, ahts, rsv, rv, psv, plsv |
| active    | bool   | Whether the vessel is active         |
| created_at | datetime | Creation timestamp                 |

### Oil Feature

| Field              | Type     | Description                              |
|--------------------|----------|------------------------------------------|
| id                 | UUID     | Primary key                              |
| latitude           | float    | -90 to 90                                |
| longitude          | float    | -180 to 180                              |
| estimated_area     | float    | m²                                       |
| confidence_level   | int      | 0–100                                    |
| status             | enum     | DETECTED, CONFIRMED, DISCARDED            |
| detection_date     | datetime | When the feature was detected             |
| confirmed_by       | UUID     | FK to User (who confirmed)               |
| confirmation_date  | datetime | When it was confirmed                     |

### Association: Oil Feature ↔ Vessel

Many-to-many via table `oil_feature_vessels`:

- `oil_feature_id` (UUID)
- `vessel_mmsi` (string, 9 chars)

Composite primary key: `(oil_feature_id, vessel_mmsi)`.

---

## Business Rules

- **Coordinates**: Latitude ∈ [-90, 90], longitude ∈ [-180, 180].
- **Confidence**: 0–100.
- **Users**: Only **active** users can confirm oil features. Cannot delete a user who has confirmed any feature.
- **Vessels**: Cannot delete a vessel that is linked to any oil feature. Cannot associate a feature with an **inactive** vessel.
- **Oil features**:
  - **Confirm**: Only active users; feature must be in DETECTED state.
  - **Discard**: Only **admin** users.
  - **Update**: Cannot update a feature that is already CONFIRMED or DISCARDED.

---

## API Reference

Base URL (local): `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

### Authentication

| Method | Endpoint       | Auth | Description        |
|--------|----------------|------|--------------------|
| POST   | `/auth/login`  | No   | Login; returns JWT |

**Request body:** `{ "email": "...", "password": "..." }`  
**Response:** `{ "access_token": "...", "token_type": "bearer" }`

Use the token in the header: `Authorization: Bearer <token>`.

### Users

| Method | Endpoint      | Auth              | Description     |
|--------|---------------|-------------------|-----------------|
| POST   | `/users/`     | No                | Create user     |
| GET    | `/users/`     | Admin             | List users      |
| GET    | `/users/{id}` | Admin             | Get user by ID  |
| PUT    | `/users/{id}` | Operator or Admin | Update user     |
| DELETE | `/users/{id}` | Admin             | Delete user     |

Create body: `name`, `email`, `password`, `role` (optional, default `operator`).

### Vessels

| Method | Endpoint          | Auth              | Description      |
|--------|-------------------|-------------------|------------------|
| GET    | `/vessels/`       | Token             | List vessels     |
| GET    | `/vessels/{mmsi}` | Token             | Get by MMSI      |
| POST   | `/vessels/`       | Operator or Admin | Create vessel    |
| PUT    | `/vessels/{mmsi}` | Operator or Admin | Update vessel    |
| DELETE | `/vessels/{mmsi}` | Admin             | Delete vessel    |

MMSI must be exactly 9 numeric digits.

### Oil Features

| Method | Endpoint                                    | Auth              | Description              |
|--------|---------------------------------------------|-------------------|--------------------------|
| GET    | `/oil-features/`                            | Token             | List (optional filters)  |
| GET    | `/oil-features/{id}`                        | Token             | Get by ID                |
| POST   | `/oil-features/`                            | Operator or Admin | Create feature           |
| PATCH  | `/oil-features/{id}`                        | Operator or Admin | Update feature           |
| DELETE | `/oil-features/{id}`                        | Admin             | Delete feature           |
| PATCH  | `/oil-features/{id}/confirm`                | Operator or Admin | Confirm feature          |
| PATCH  | `/oil-features/{id}/discard`                | Admin             | Discard feature          |
| POST   | `/oil-features/{id}/vessels/{mmsi}`         | Admin             | Associate vessel         |
| DELETE | `/oil-features/{id}/vessels/{mmsi}`         | Admin             | Disassociate vessel      |

**List filters (query params):** `status`, `min_confidence_level`

---

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 15 (or use Docker)
- Docker & Docker Compose (optional, for containerized run)

### 1. Clone and install dependencies

```bash
git clone <repository-url>
cd gestao-feicoes-maritimas
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Environment variables

Create a `.env` in the project root:

```env
DB_URL=postgresql://postgres:postgres@localhost:5432/gestao_feicoes
SECRET_KEY=your-secret-key-for-jwt
ALGORITHM=HS256
ACESS_TOKEN_EXPIRE_MINUTES=120
```

Adjust `DB_URL` if your PostgreSQL user, password, host, or database name differ.

### 3. Database and migrations

Ensure PostgreSQL is running, then:

```bash
alembic upgrade head
```

### 4. Run the API (local)

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000  
- Swagger UI: http://localhost:8000/docs  

### 5. Run with Docker Compose

Starts PostgreSQL and the API in containers:

```bash
docker compose up -d
```

Apply migrations after containers are up:

```bash
docker exec gestao-feicoes-maritimas-api-1 alembic upgrade head
```

Optional `.env` for Compose:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=gestao_feicoes
SECRET_KEY=change-me-in-production
```

- API: http://localhost:8000  
- DB: localhost:5432 (user/password/database as in `DB_USER`/`DB_PASSWORD`/`DB_NAME`)

### 6. Quick test

1. Create a user: `POST /users/` with `name`, `email`, `password`, `role` (e.g. `admin`).
2. Login: `POST /auth/login` with JSON body (`email`, `password`) or OAuth2 form body (`username`, `password`) from Swagger Authorize.
3. Use the returned `access_token` in `Authorization: Bearer <token>` for protected endpoints.

---

## Database & Migrations

- **ORM**: SQLAlchemy; models live under `src/infrastructure/database/models/`.
- **Migrations**: Alembic; scripts in `alembic/versions/`.

Commands:

```bash
# Apply all migrations
alembic upgrade head

# Create a new migration (after changing models)
alembic revision --autogenerate -m "description"

# Rollback one revision
alembic downgrade -1
```

Initial migration creates `users`, `vessels`, `oil_features`, and `oil_feature_vessels`. A later migration standardizes oil feature status values to English (DETECTED, CONFIRMED, DISCARDED).

---

## Testing

### Unit tests (domain entities)

No database required:

```bash
pytest tests/unit/ -v
```

Covers entity rules (e.g. user/vessel delete validation, oil feature defaults).

### Integration test (full flow)

Requires PostgreSQL and `DB_URL` pointing to it (e.g. after `docker compose up -d db`):

```bash
# Set DB_URL if not in .env
set DB_URL=postgresql://postgres:postgres@localhost:5432/gestao_feicoes   # Windows CMD
$env:DB_URL="postgresql://postgres:postgres@localhost:5432/gestao_feicoes" # Windows PowerShell
export DB_URL=postgresql://postgres:postgres@localhost:5432/gestao_feicoes # Linux/macOS

pytest tests/integration/ -v
```

The integration test:

1. Creates an admin user and logs in.
2. Creates two vessels.
3. Creates an oil feature.
4. Associates the feature with both vessels.
5. Confirms the feature.
6. Asserts final state (status CONFIRMED, `confirmed_by`, `confirmation_date`, and basic fields).

If `DB_URL` is unset or SQLite, the integration test is skipped.

---

## Project Structure

```
gestao-feicoes-maritimas/
├── alembic/
│   ├── env.py                    # Alembic config, uses DB_URL from env
│   └── versions/                 # Migration scripts
├── src/
│   ├── api/
│   │   ├── main.py               # FastAPI app, router registration
│   │   └── dependencies.py       # get_db, repositories, services, auth (JWT, require_admin, etc.)
│   ├── core/
│   │   ├── database.py           # SQLAlchemy engine, SessionLocal, get_db
│   │   └── security.py           # bcrypt hash/verify, JWT create/verify
│   ├── domain/
│   │   ├── entities/             # User, Vessel, OilFeature (domain models)
│   │   └── interfaces/           # IUserRepository, IVesselRepository, IOilFeatureRepository
│   ├── infrastructure/
│   │   ├── database/
│   │   │   └── models/           # SQLAlchemy models (UserModel, VesselModel, OilFeatureModel)
│   │   └── repositories/        # UserRepository, VesselRepository, OilFeatureRepository
│   ├── routers/
│   │   ├── auth_router.py        # POST /auth/login
│   │   ├── user_router.py        # /users
│   │   ├── vessel_router.py      # /vessels
│   │   └── oil_feature_router.py # /oil-features
│   ├── schemas/                  # Pydantic DTOs (UserCreateDTO, VesselDTO, OilFeatureDTO, etc.)
│   └── services/                 # UserService, VesselService, OilFeatureService, AuthService,
│                                 # AssociateOilFeatureService, ConfirmOilFeatureService, DiscardOilFeatureService
├── tests/
│   ├── conftest.py               # Pytest env defaults
│   ├── unit/
│   │   └── domain/entities/       # test_user, test_vessel, test_oil_feature
│   └── integration/
│       └── test_oil_feature_flow.py  # Full flow: create feature, associate vessels, confirm
├── compose.yaml                  # PostgreSQL + API services
├── Dockerfile                    # Python 3.12, uvicorn
├── alembic.ini
├── requirements.txt
└── README.md
```

---
