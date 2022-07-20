"""add foreign key in task table

Revision ID: 89bace7c2834
Revises: cf0e36da27c0
Create Date: 2022-07-20 10:29:19.141903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89bace7c2834'
down_revision = 'cf0e36da27c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key('task_user_fk', source_table="tasks", referent_table="users",  local_cols=[
                          'user_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('task_user_fk', table_name='tasks')
