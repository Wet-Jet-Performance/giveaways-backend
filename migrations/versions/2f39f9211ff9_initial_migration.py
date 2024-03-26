"""initial migration

Revision ID: 2f39f9211ff9
Revises: 
Create Date: 2024-03-25 15:04:13.434240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f39f9211ff9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone_number', sa.Text(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('giveaway',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start_date_time', sa.DateTime(), nullable=True),
    sa.Column('end_date_time', sa.DateTime(), nullable=True),
    sa.Column('winning_entry_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['winning_entry_id'], ['contact_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('giveaway_ticket',
    sa.Column('ticket_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('giveaway_id', sa.Integer(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contact_info.id'], ),
    sa.ForeignKeyConstraint(['giveaway_id'], ['giveaway.id'], ),
    sa.PrimaryKeyConstraint('ticket_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('giveaway_ticket')
    op.drop_table('giveaway')
    op.drop_table('contact_info')
    # ### end Alembic commands ###
