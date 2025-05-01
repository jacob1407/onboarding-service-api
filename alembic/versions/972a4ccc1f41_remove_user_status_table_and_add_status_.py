"""remove user_status table and add status to user_model

Revision ID: 972a4ccc1f41
Revises: 340f5338cf67
Create Date: 2025-05-01 18:40:23.168234

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "972a4ccc1f41"
down_revision: Union[str, None] = "340f5338cf67"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Define the enums
    user_status_enum = sa.Enum(
        "active", "invited", "inactive", "archived", name="userstatus"
    )
    user_type_enum = sa.Enum("admin", "employee", name="usertype")

    # Create the enum types in the database
    user_status_enum.create(op.get_bind(), checkfirst=True)
    user_type_enum.create(op.get_bind(), checkfirst=True)

    # Drop old table
    op.drop_table("user_status")

    # Add new columns using the created enum types
    op.add_column("users", sa.Column("status", user_status_enum, nullable=False))
    op.add_column("users", sa.Column("type", user_type_enum, nullable=False))


def downgrade() -> None:
    op.drop_column("users", "type")
    op.drop_column("users", "status")

    # Drop enums (optional, safe if no longer used elsewhere)
    sa.Enum(name="usertype").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="userstatus").drop(op.get_bind(), checkfirst=True)

    op.create_table(
        "user_status",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "active", "invited", "inactive", "archived", name="userstatus"
            ),
            nullable=False,
        ),
        sa.Column(
            "last_updated_date",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("user_id"),
    )
