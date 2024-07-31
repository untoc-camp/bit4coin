"""empty message

Revision ID: 209e7b93dc26
Revises: dc8d8be5e9ac
Create Date: 2024-07-31 16:02:36.144473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '209e7b93dc26'
down_revision = 'dc8d8be5e9ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('api_key', sa.Text(), nullable=False),
    sa.Column('api_key_secret', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_user_name'), 'users', ['user_name'], unique=True)
    op.drop_table('user')
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.create_foreign_key(None, 'item', 'users', ['onwer_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.create_foreign_key(None, 'item', 'user', ['onwer_id'], ['id'])
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_name', sa.VARCHAR(), nullable=False),
    sa.Column('password', sa.TEXT(), nullable=False),
    sa.Column('balance', sa.FLOAT(), nullable=False),
    sa.Column('api_key', sa.TEXT(), nullable=False),
    sa.Column('api_secret', sa.TEXT(), nullable=False),
    sa.Column('create_date', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index(op.f('ix_users_user_name'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###