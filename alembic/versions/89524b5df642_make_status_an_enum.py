"""Make status an enum

Revision ID: 89524b5df642
Revises: 97c1e3f75233
Create Date: 2025-05-05 20:58:15.065310

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "89524b5df642"
down_revision: Union[str, None] = "97c1e3f75233"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define enum matching the Python Enum
employee_onboarding_status_enum = postgresql.ENUM(
    "pending", "in_progress", "complete", "cancelled", name="employeeonboardingstatus"
)


def upgrade() -> None:
    """Upgrade schema."""
    # Create the enum type in the database
    employee_onboarding_status_enum.create(op.get_bind(), checkfirst=True)

    # Alter the column to use the enum type
    op.alter_column(
        "employee_onboarding_requests",
        "status",
        existing_type=sa.VARCHAR(),
        type_=employee_onboarding_status_enum,
        existing_nullable=False,
        postgresql_using="status::text::employeeonboardingstatus",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert column back to VARCHAR
    op.alter_column(
        "employee_onboarding_requests",
        "status",
        existing_type=employee_onboarding_status_enum,
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="status::text",
    )

    # Drop the enum type from the database
    employee_onboarding_status_enum.drop(op.get_bind(), checkfirst=True)
