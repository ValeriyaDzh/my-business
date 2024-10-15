"""rename col

Revision ID: 6de53eb36a9f
Revises: 857c8fdf4d80
Create Date: 2024-10-15 16:09:23.413460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6de53eb36a9f'
down_revision: Union[str, None] = '857c8fdf4d80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(), nullable=False))
    op.add_column('user', sa.Column('is_verified', sa.Boolean(), nullable=False))
    op.drop_constraint('user_account_key', 'user', type_='unique')
    op.create_unique_constraint(None, 'user', ['email'])
    op.drop_column('user', 'account')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('account', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user', type_='unique')
    op.create_unique_constraint('user_account_key', 'user', ['account'])
    op.drop_column('user', 'is_verified')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###