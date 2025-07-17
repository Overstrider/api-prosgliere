"""Initial create tables

Revision ID: initial
Revises: 
Create Date: 2023-12-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('blog_posts',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('post_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['blog_posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('comments')
    op.drop_table('blog_posts') 