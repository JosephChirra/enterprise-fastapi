"""add is_active to users

Revision ID: 0f8a38962ed1
Revises: 125d54cf828a
Create Date: 2026-11-25 11:24:48.538282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f8a38962ed1'
down_revision: Union[str, Sequence[str], None] = '125d54cf828a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        )
    )

def downgrade() -> None:
    op.drop_column('users', 'is_active')