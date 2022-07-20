"""create post table

Revision ID: ecac1c06547e
Revises: 
Create Date: 2022-07-20 10:16:40.281065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecac1c06547e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('tasks',
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("title", sa.String(), nullable=False),
                    sa.Column("description", sa.String(), nullable=False),
                    sa.Column("completed", sa.Boolean(),
                              server_default='False', nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column("user_id", sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:

    op.drop_table('tasks')
