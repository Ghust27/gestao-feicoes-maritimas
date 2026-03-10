"""Standardize oil feature status values from Portuguese to English.

Revision ID: a1b2c3d4e5f6
Revises: 0ac366912ad2
Create Date: 2026-03-09

"""
from typing import Sequence, Union

from alembic import op


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "0ac366912ad2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE oil_features SET status = 'DETECTED' WHERE status = 'DETECTADA'")
    op.execute("UPDATE oil_features SET status = 'CONFIRMED' WHERE status = 'CONFIRMADA'")
    op.execute("UPDATE oil_features SET status = 'DISCARDED' WHERE status = 'DESCARTADA'")


def downgrade() -> None:
    op.execute("UPDATE oil_features SET status = 'DETECTADA' WHERE status = 'DETECTED'")
    op.execute("UPDATE oil_features SET status = 'CONFIRMADA' WHERE status = 'CONFIRMED'")
    op.execute("UPDATE oil_features SET status = 'DESCARTADA' WHERE status = 'DISCARDED'")
