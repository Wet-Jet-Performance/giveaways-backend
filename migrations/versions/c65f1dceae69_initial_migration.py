"""initial migration

Revision ID: c65f1dceae69
Revises: 
Create Date: 2024-04-01 16:33:51.708459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c65f1dceae69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticket',
    sa.Column('giveaway_id', sa.Integer(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('number_of_tickets', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['giveaway_id'], ['giveaway.id'], ),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
    sa.PrimaryKeyConstraint('giveaway_id', 'participant_id')
    )
    op.create_table('winner',
    sa.Column('giveaway_id', sa.Integer(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['giveaway_id'], ['giveaway.id'], ),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
    sa.PrimaryKeyConstraint('giveaway_id', 'participant_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('winner')
    op.drop_table('ticket')
    # ### end Alembic commands ###