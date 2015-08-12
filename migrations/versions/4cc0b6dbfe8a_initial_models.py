# 4cc0b6dbfe8a_initial_models
# Initial migration for the original models for Inigo
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jul 05 16:45:00 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: 4cc0b6dbfe8a_initial_models.py [] benjamin@bengfort.com $

"""
Initial migration for the original models for Inigo.

Revision ID: 4cc0b6dbfe8a
Revises:     None
Create Date: 2015-07-05 16:42:34.114954
"""

##########################################################################
## Revision Identifiers, used by Alembic.
##########################################################################

revision      = '4cc0b6dbfe8a'
down_revision = None
branch_labels = None
depends_on    = None

##########################################################################
## Imports
##########################################################################

from alembic import op
import sqlalchemy as sa

##########################################################################
## Upgrade and Downgrade commands
##########################################################################

def upgrade():
    op.create_table('pictures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('signature', sa.Unicode(length=44), nullable=False),
        sa.Column('date_taken', sa.DateTime(timezone=True), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('description', sa.UnicodeText(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('signature')
    )

    op.create_table('storages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hostname', sa.Unicode(length=255), nullable=True),
        sa.Column('filepath', sa.Unicode(length=512), nullable=False),
        sa.Column('picture_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['picture_id'], ['pictures.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('storages')
    op.drop_table('pictures')
