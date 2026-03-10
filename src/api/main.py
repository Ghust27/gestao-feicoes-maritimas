from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError, ProgrammingError

from src.routers import auth_router, oil_feature_router, user_router, vessel_router

app = FastAPI(title="API for Maritime Feature Management.", version="1.0.0")
app.include_router(auth_router.router)
app.include_router(oil_feature_router.router)
app.include_router(vessel_router.router)
app.include_router(user_router.router)


@app.exception_handler(OperationalError)
@app.exception_handler(ProgrammingError)
async def db_exception_handler(request: Request, exc: Exception):
    """Return 503 when database is unavailable or schema is missing."""
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Database unavailable or not migrated. Run: alembic upgrade head",
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Ensure unhandled exceptions return JSON and do not leak internals."""
    if isinstance(exc, HTTPException):
        raise exc
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error."},
    )


@app.get("/")
def root():
    return {"message": "Welcome to the Marine Feature Management API."}