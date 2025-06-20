"""Revision script: ${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""

from typing import Sequence
from alembic import op
import sqlalchemy as sa

${imports if imports else ""}

# Alembic revision identifiers
revision: str = ${repr(up_revision)}
down_revision: str | Sequence[str] | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}

__all__ = ["upgrade", "downgrade"]

# --- Helpers (optional) ---
# def now() -> sa.sql.expression.Function:
#     return sa.func.now()

# --- Upgrade ---
def upgrade() -> None:
    """Apply schema changes."""
    # ### Alembic auto-generated upgrades ###
    ${upgrades if upgrades else "pass"}
    # ### end Alembic upgrades ###

# --- Downgrade ---
def downgrade() -> None:
    """Revert schema changes."""
    # ### Alembic auto-generated downgrades ###
    ${downgrades if downgrades else "pass"}
    # ### end Alembic downgrades ###
