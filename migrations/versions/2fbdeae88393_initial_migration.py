"""Initial migration.

Revision ID: 2fbdeae88393
Revises: c5128cf1282e
Create Date: 2024-07-03 18:51:22.304699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fbdeae88393'
down_revision = 'c5128cf1282e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dynamic_data', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dynamic_data', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###
