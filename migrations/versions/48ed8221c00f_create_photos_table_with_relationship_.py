"""create photos table with relationship to giveaways

Revision ID: 48ed8221c00f
Revises: 667cd047c345
Create Date: 2024-05-22 15:06:34.080778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48ed8221c00f'
down_revision = '667cd047c345'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('photo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('giveaway_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['giveaway_id'], ['giveaway.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('photo')
    # ### end Alembic commands ###