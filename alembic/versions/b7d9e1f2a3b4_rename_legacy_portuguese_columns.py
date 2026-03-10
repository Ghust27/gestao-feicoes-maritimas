"""Rename legacy Portuguese column names to English.

Revision ID: b7d9e1f2a3b4
Revises: a1b2c3d4e5f6
Create Date: 2026-03-09

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b7d9e1f2a3b4"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _rename_if_needed(table: str, old: str, new: str) -> None:
    op.execute(
        f"""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = '{table}'
                  AND column_name = '{old}'
            ) AND NOT EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = '{table}'
                  AND column_name = '{new}'
            ) THEN
                EXECUTE 'ALTER TABLE {table} RENAME COLUMN {old} TO {new}';
            END IF;
        END
        $$;
        """
    )


def upgrade() -> None:
    _rename_if_needed("users", "nome", "name")
    _rename_if_needed("users", "ativo", "active")

    _rename_if_needed("vessels", "nome", "name")
    _rename_if_needed("vessels", "tipo", "vessel_type")
    _rename_if_needed("vessels", "ativo", "active")

    _rename_if_needed("oil_features", "area_estimada_m2", "estimated_area")
    _rename_if_needed("oil_features", "nivel_confianca", "confidence_level")
    _rename_if_needed("oil_features", "data_deteccao", "detection_date")
    _rename_if_needed("oil_features", "confirmada_por", "confirmed_by")
    _rename_if_needed("oil_features", "data_confirmacao", "confirmation_date")


def downgrade() -> None:
    _rename_if_needed("users", "name", "nome")
    _rename_if_needed("users", "active", "ativo")

    _rename_if_needed("vessels", "name", "nome")
    _rename_if_needed("vessels", "vessel_type", "tipo")
    _rename_if_needed("vessels", "active", "ativo")

    _rename_if_needed("oil_features", "estimated_area", "area_estimada_m2")
    _rename_if_needed("oil_features", "confidence_level", "nivel_confianca")
    _rename_if_needed("oil_features", "detection_date", "data_deteccao")
    _rename_if_needed("oil_features", "confirmed_by", "confirmada_por")
    _rename_if_needed("oil_features", "confirmation_date", "data_confirmacao")
