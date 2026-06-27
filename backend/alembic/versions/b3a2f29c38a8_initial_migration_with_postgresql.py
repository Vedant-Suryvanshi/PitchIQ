"""Initial migration with PostgreSQL

Revision ID: b3a2f29c38a8
Revises: 
Create Date: 2026-06-26 13:44:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b3a2f29c38a8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply the migration."""
    # Create enum type for job status
    op.execute("CREATE TYPE jobstatus AS ENUM ('queued', 'running', 'completed', 'failed')")
    op.execute("CREATE TYPE jobstatus AS ENUM ('queued', 'running', 'completed', 'failed')")
    
    # Create memo_jobs table
    op.create_table(
        'memo_jobs',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('startup_description', sa.Text(), nullable=False),
        sa.Column('status', sa.Enum('queued', 'running', 'completed', 'failed', name='jobstatus'), nullable=False),
        sa.Column('agent_progress', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("length(id) = 36", name='check_id_length')
    )
    
    # Create indexes for memo_jobs
    op.create_index('ix_memo_jobs_status', 'memo_jobs', ['status'])
    op.create_index('ix_memo_jobs_created_at', 'memo_jobs', ['created_at'])
    op.create_index('ix_memo_jobs_updated_at', 'memo_jobs', ['updated_at'])
    op.create_index('ix_memo_jobs_status_created', 'memo_jobs', ['status', 'created_at'])
    
    # Create memo_results table
    op.create_table(
        'memo_results',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('job_id', sa.String(36), nullable=False),
        sa.Column('startup_name', sa.String(255), nullable=True),
        sa.Column('industry', sa.String(255), nullable=True),
        sa.Column('business_model', sa.String(255), nullable=True),
        sa.Column('target_users', sa.String(255), nullable=True),
        sa.Column('geography', sa.String(255), nullable=True),
        sa.Column('market_research_output', sa.Text(), nullable=True),
        sa.Column('funding_analysis_output', sa.Text(), nullable=True),
        sa.Column('memo_markdown', sa.Text(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('quality_flags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['job_id'], ['memo_jobs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('job_id')
    )
    
    # Create indexes for memo_results
    op.create_index('ix_memo_results_job_id', 'memo_results', ['job_id'])
    op.create_index('ix_memo_results_created_at', 'memo_results', ['created_at'])
    op.create_index('ix_memo_results_confidence_score', 'memo_results', ['confidence_score'])
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.Column('api_keys', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    
    # Create indexes for users
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_username', 'users', ['username'])
    op.create_index('ix_users_created_at', 'users', ['created_at'])


def downgrade() -> None:
    """Revert the migration."""
    # Drop tables in reverse order
    op.drop_table('users')
    op.drop_table('memo_results')
    op.drop_table('memo_jobs')
    
    # Drop enum type
    op.execute("DROP TYPE jobstatus")