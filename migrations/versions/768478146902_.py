"""empty message

Revision ID: 768478146902
Revises: 3ae58f5b963b
Create Date: 2023-07-05 12:27:31.306845

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '768478146902'
down_revision = '3ae58f5b963b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meme', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_posted', sa.DateTime(), nullable=True))
        batch_op.drop_column('date_posteed')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meme', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_posteed', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.drop_column('date_posted')

    # ### end Alembic commands ###