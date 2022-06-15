"""Create patients Table

Revision ID: 4b58c08e58f9
Revises: 5acc4ff2721c
Create Date: 2022-06-11 13:00:34.446040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b58c08e58f9'
down_revision = '5acc4ff2721c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("patients", 
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("full_name", sa.String(length=255), nullable=False),
                    sa.Column("date_of_birth", sa.Integer(), nullable=False),
                    sa.Column("phone_number", sa.String(length=255), nullable=False),
                    sa.Column("gender", sa.Integer(), nullable=False),
                    sa.Column("current_location", sa.String, nullable = False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("role", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
                    sa.Column("creator_id", sa.Integer(), nullable=False),
                    sa.UniqueConstraint("email"),
                    sa.ForeignKeyConstraint(["creator_id"], ["admins.id"], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint("id")
                    )
    pass


def downgrade():
    op.drop_table("patients")
    pass
