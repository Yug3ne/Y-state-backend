"""token list migration updated

Revision ID: 5483a48c4639
Revises: 343d07323c8e
Create Date: 2024-07-04 15:15:18.204432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5483a48c4639'
down_revision = '343d07323c8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tokenblocklist', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tokenblocklist', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###
