"""update user

Revision ID: bb1257b6edc4
Revises: c32d3f8d33b9
Create Date: 2021-07-15 16:25:34.963075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb1257b6edc4'
down_revision = 'c32d3f8d33b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('batch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(length=140), nullable=True),
    sa.Column('waktu', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_batch_timestamp'), 'batch', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_batch_timestamp'), table_name='batch')
    op.drop_table('batch')
    # ### end Alembic commands ###
