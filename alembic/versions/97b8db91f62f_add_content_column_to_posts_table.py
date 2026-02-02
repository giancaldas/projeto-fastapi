"""add content column to posts table

Revision ID: 97b8db91f62f
Revises: 52161eaa5acf
Create Date: 2026-01-29 15:32:07.381194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97b8db91f62f'
down_revision: Union[str, Sequence[str], None] = '52161eaa5acf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
