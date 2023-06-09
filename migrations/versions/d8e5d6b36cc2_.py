"""empty message

Revision ID: d8e5d6b36cc2
Revises: 71c0f8fb556b
Create Date: 2023-07-08 21:00:22.162505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8e5d6b36cc2'
down_revision = '71c0f8fb556b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meme', schema=None) as batch_op:
        batch_op.alter_column('public',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meme', schema=None) as batch_op:
        batch_op.alter_column('public',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###
