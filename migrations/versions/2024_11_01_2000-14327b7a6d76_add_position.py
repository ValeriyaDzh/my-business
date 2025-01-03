"""add Position

Revision ID: 14327b7a6d76
Revises: 477b44955f68
Create Date: 2024-11-01 20:00:25.172294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14327b7a6d76'
down_revision: Union[str, None] = '477b44955f68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('position',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('company_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_position_id'), 'position', ['id'], unique=False)
    op.add_column('user', sa.Column('department_id', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('position_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'department', ['department_id'], ['id'])
    op.create_foreign_key(None, 'user', 'position', ['position_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'position_id')
    op.drop_column('user', 'department_id')
    op.drop_index(op.f('ix_position_id'), table_name='position')
    op.drop_table('position')
    # ### end Alembic commands ###
