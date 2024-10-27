"""
First migration

Revision ID: a0240bd26827
Revises:
Create Date: 2024-10-27 15:06:16.087741

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a0240bd26827"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("user",
    sa.Column("id", sa.BigInteger(), nullable=False),
    sa.Column("username", sa.String(), nullable=False),
    sa.Column("joined_us", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    sa.Column("last_activity", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    sa.Column("is_admin", sa.Boolean(), nullable=False),
    sa.Column("is_superuser", sa.Boolean(), nullable=False),
    sa.Column("is_banned", sa.Boolean(), nullable=False),
    sa.Column("language", sa.Enum("EN", "RU", name="languagelocale"), nullable=False),
    sa.PrimaryKeyConstraint("id")
    )
    op.create_table("username",
    sa.Column("id", sa.Uuid(), nullable=False),
    sa.Column("value", sa.String(), nullable=False),
    sa.Column("status", sa.Enum("AVAILABLE", "NOT_AVAILABLE", "UNKNOWN", name="usernamestatus"), nullable=False),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("value")
    )
    op.create_table("subscription",
    sa.Column("id", sa.Uuid(), nullable=False),
    sa.Column("interval", sa.Enum("MINUTE", "MINUTE_30", "HOUR", "DAY", name="interval"), nullable=False),
    sa.Column("subscriber_id", sa.BigInteger(), nullable=False),
    sa.Column("username_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(["subscriber_id"], ["user.id"], ),
    sa.ForeignKeyConstraint(["username_id"], ["username.id"], ),
    sa.PrimaryKeyConstraint("id")
    )
    op.create_table("username_user_assoc",
    sa.Column("username_id", sa.Uuid(), nullable=False),
    sa.Column("user_id", sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(["user_id"], ["user.id"], ),
    sa.ForeignKeyConstraint(["username_id"], ["username.id"], ),
    sa.PrimaryKeyConstraint("username_id", "user_id")
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("username_user_assoc")
    op.drop_table("subscription")
    op.drop_table("username")
    op.drop_table("user")
    # ### end Alembic commands ###