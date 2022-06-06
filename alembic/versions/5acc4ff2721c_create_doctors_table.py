"""create doctors table

Revision ID: 5acc4ff2721c
Revises: 4626da1feb07
Create Date: 2022-06-05 20:50:27.951649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5acc4ff2721c'
down_revision = '4626da1feb07'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("doctors", 
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("name", sa.String(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("field", sa.String(), nullable=False),
                    sa.Column("role", sa.String(), nullable=False, server_default="doctor"),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text("now()"), nullable=False),
                    sa.Column("creator_id", sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"),
                    sa.ForeignKeyConstraint(["creator_id"], ["admins.id"], ondelete="CASCADE"),
                    )

    pass


def downgrade():
    op.drop_table("doctors")
    pass
