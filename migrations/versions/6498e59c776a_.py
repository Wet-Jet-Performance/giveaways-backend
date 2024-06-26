"""empty message

Revision ID: 6498e59c776a
Revises: 
Create Date: 2024-06-15 17:05:20.729080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6498e59c776a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('giveaway',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone_number', sa.Text(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cloudflare_id', sa.String(), nullable=True),
    sa.Column('giveaway_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['giveaway_id'], ['giveaway.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('giveaway_id', sa.Integer(), nullable=True),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['giveaway_id'], ['giveaway.id'], ),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('winner',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('winning_ticket_id', sa.Integer(), nullable=True),
    sa.Column('giveaway_id', sa.Integer(), nullable=True),
    sa.Column('participant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['giveaway_id'], ['giveaway.id'], ),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
    sa.ForeignKeyConstraint(['winning_ticket_id'], ['ticket.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('winner')
    op.drop_table('ticket')
    op.drop_table('photo')
    op.drop_table('participant')
    op.drop_table('giveaway')
    # ### end Alembic commands ###
