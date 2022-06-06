"""create admins table

Revision ID: 4626da1feb07
Revises: 
Create Date: 2022-06-05 19:55:03.736300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4626da1feb07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("admins", 
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("name", sa.String(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("role", sa.String(), nullable=False, server_default="admin"),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade():
    op.drop_table("admins")
    pass
