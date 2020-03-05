"""empty message

Revision ID: 6de63a613120
Revises: 40470d468dcd
Create Date: 2020-03-05 18:59:21.590765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6de63a613120'
down_revision = '40470d468dcd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('guest', sa.Column('email_id', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_guest_email_id'), 'guest', ['email_id'], unique=True)
    op.drop_index('ix_guest_phone_number', table_name='guest')
    op.drop_column('guest', 'phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('guest', sa.Column('phone_number', sa.VARCHAR(length=64), nullable=True))
    op.create_index('ix_guest_phone_number', 'guest', ['phone_number'], unique=1)
    op.drop_index(op.f('ix_guest_email_id'), table_name='guest')
    op.drop_column('guest', 'email_id')
    # ### end Alembic commands ###
