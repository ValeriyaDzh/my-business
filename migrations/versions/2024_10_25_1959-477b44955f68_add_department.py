"""add Department

Revision ID: 477b44955f68
Revises: d38f56ea732f
Create Date: 2024-10-25 19:59:52.778025

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy_utils
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "477b44955f68"
down_revision: Union[str, None] = "d38f56ea732f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "department",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("path", sqlalchemy_utils.types.ltree.LtreeType(), nullable=False),
        sa.Column("company_id", sa.UUID(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company.id"],
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["department.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_departments_path",
        "department",
        ["path"],
        unique=False,
        postgresql_using="gist",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "ix_departments_path", table_name="department", postgresql_using="gist"
    )
    op.drop_table("department")
    # ### end Alembic commands ###
