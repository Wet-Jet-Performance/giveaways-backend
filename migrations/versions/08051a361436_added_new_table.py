"""added new table.

Revision ID: 08051a361436
Revises: 2fbdeae88393
Create Date: 2024-07-04 18:03:27.965699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08051a361436'
down_revision = '2fbdeae88393'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('giveaway_steps',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('step_number', sa.String(), nullable=True),
    sa.Column('step_title', sa.String(), nullable=True),
    sa.Column('step_description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('giveaway_steps')
    # ### end Alembic commands ###
