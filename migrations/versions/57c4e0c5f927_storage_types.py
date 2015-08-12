"""storage types

Revision ID: 57c4e0c5f927
Revises: 381edcdc3cbe
Create Date: 2015-08-12 15:27:04.143873

"""

# revision identifiers, used by Alembic.
revision = '57c4e0c5f927'
down_revision = '381edcdc3cbe'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

STYPE = ('ORIGINAL', 'BACKUP', 'CLOUD', 'DROBO')
STYPE = sa.Enum(*STYPE, name='STORAGE_TYPE')

def upgrade():
    STYPE.create(op.get_bind(), checkfirst=False)
    op.add_column('storages', sa.Column('memo', sa.Unicode(length=255), nullable=True))
    op.add_column('storages', sa.Column('stype', sa.Enum('ORIGINAL', 'BACKUP', 'CLOUD', 'DROBO', name='STORAGE_TYPE'), nullable=True))


def downgrade():
    op.drop_column('storages', 'stype')
    op.drop_column('storages', 'memo')
    STYPE.drop(oop.get_bind(), checkfirst=False)
