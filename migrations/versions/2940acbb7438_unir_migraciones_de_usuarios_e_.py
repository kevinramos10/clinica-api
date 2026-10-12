"""unir migraciones de usuarios e historiales

Revision ID: 2940acbb7438
Revises: 133a6b48667d, 3a15a03c4722
Create Date: 2026-10-09 17:36:12.583339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2940acbb7438'
down_revision = ('133a6b48667d', '3a15a03c4722')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
