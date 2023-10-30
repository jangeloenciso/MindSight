"""empty message

Revision ID: c7ba76ab2c7a
Revises: 46b1041143f5
Create Date: 2023-10-31 04:58:00.582634

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c7ba76ab2c7a'
down_revision = '46b1041143f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student_information', schema=None) as batch_op:
        batch_op.drop_column('college_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student_information', schema=None) as batch_op:
        batch_op.add_column(sa.Column('college_id', mysql.INTEGER(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
