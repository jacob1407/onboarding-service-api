"""Make status an enum v2

Revision ID: 24de8a9eca0e
Revises: 2154ae66ad0f
Create Date: 2025-05-05 21:10:36.865674

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "24de8a9eca0e"
down_revision: Union[str, None] = "2154ae66ad0f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


employee_onboarding_request_status_enum = postgresql.ENUM(
    "requested", "complete", "denie", name="employeeonboardingrequeststatus"
)


def upgrade() -> None:
    """Upgrade schema."""
    # Create the enum type in the database
    employee_onboarding_request_status_enum.create(op.get_bind(), checkfirst=True)

    # Alter the column to use the enum type
    op.alter_column(
        "employee_onboarding_requests",
        "status",
        existing_type=sa.VARCHAR(),
        type_=employee_onboarding_request_status_enum,
        existing_nullable=False,
        postgresql_using="status::text::employeeonboardingrequeststatus",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert column back to VARCHAR
    op.alter_column(
        "employee_onboarding_requests",
        "status",
        existing_type=employee_onboarding_request_status_enum,
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="status::text",
    )

    # Drop the enum type from the database
    employee_onboarding_request_status_enum.drop(op.get_bind(), checkfirst=True)
