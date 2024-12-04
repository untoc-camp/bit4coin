"""remove cur_price

Revision ID: dc8d8be5e9ac
Revises: 8d2723fff816
Create Date: 2024-07-15 21:52:35.980758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc8d8be5e9ac'
down_revision = '8d2723fff816'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("item", "cur_price")

def downgrade() -> None:
    pass
