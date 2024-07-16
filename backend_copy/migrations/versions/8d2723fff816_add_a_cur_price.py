"""add a cur_price

Revision ID: 8d2723fff816
Revises: c34811630b7f
Create Date: 2024-07-15 21:45:02.973218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d2723fff816'
down_revision = 'c34811630b7f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('item', sa.Column('cur_price', sa.Float))



def downgrade() -> None:
    pass
