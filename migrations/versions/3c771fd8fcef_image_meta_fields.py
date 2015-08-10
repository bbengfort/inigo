"""image meta fields

Revision ID: 3c771fd8fcef
Revises: 4cc0b6dbfe8a
Create Date: 2015-08-09 18:16:45.717060

"""

# revision identifiers, used by Alembic.
revision = '3c771fd8fcef'
down_revision = '4cc0b6dbfe8a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pictures', sa.Column('height', sa.Integer(), nullable=True))
    op.add_column('pictures', sa.Column('mimetype', sa.Unicode(length=64), nullable=True))
    op.add_column('pictures', sa.Column('width', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pictures', 'width')
    op.drop_column('pictures', 'mimetype')
    op.drop_column('pictures', 'height')
    ### end Alembic commands ###