"""add exercisetype

Revision ID: bd56b03219fe
Revises: e4b807cb4d92
Create Date: 2026-02-04 10:58:02.608678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd56b03219fe'
down_revision: Union[str, Sequence[str], None] = 'e4b807cb4d92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to support time-based exercises."""
    
    # === EXERCISES TABLE ===
    
    # Add 'type' column to distinguish between reps-based and time-based exercises
    # Default value 'reps' ensures existing exercises remain valid
    op.add_column('exercises', sa.Column('type', sa.String(length=20), server_default='reps', nullable=False))
    
    # Explicitly update existing records to have type='reps' (redundant with server_default, but explicit is better)
    op.execute("UPDATE exercises SET type = 'reps' WHERE type IS NULL OR type = ''")
    
    # Add CHECK constraint to validate exercise type values
    op.create_check_constraint(
        'ck_exercise_type_valid',
        'exercises',
        "type IN ('reps', 'time')"
    )
    
    # === SESSION_EXERCISES TABLE ===
    
    # Add 'time_seconds' column for time-based exercises (e.g., planks, cardio)
    op.add_column('session_exercises', sa.Column('time_seconds', sa.Integer(), nullable=True))
    
    # Change 'reps' to nullable since time-based exercises don't use reps
    op.alter_column('session_exercises', 'reps',
               existing_type=sa.INTEGER(),
               nullable=True)
    
    # Check if old constraint exists before attempting to drop it
    # This prevents migration failure if constraint name is different or doesn't exist
    conn = op.get_bind()
    result = conn.execute(sa.text("""
        SELECT constraint_name 
        FROM information_schema.table_constraints 
        WHERE table_name = 'session_exercises' 
        AND constraint_name = 'ck_session_exercise_reps_positive'
    """))
    if result.fetchone():
        # Drop old constraint that required reps > 0 (doesn't work with nullable)
        op.drop_constraint('ck_session_exercise_reps_positive', 'session_exercises', type_='check')
    
    # Add new constraint: if reps is provided, it must be positive
    op.create_check_constraint(
        'ck_session_exercise_reps_positive',
        'session_exercises',
        'reps IS NULL OR reps > 0'
    )
    
    # Add constraint: if time_seconds is provided, it must be positive
    op.create_check_constraint(
        'ck_session_exercise_time_positive',
        'session_exercises',
        'time_seconds IS NULL OR time_seconds > 0'
    )
    
    # XOR constraint: exactly one of (reps, time_seconds) must be NOT NULL
    # This ensures every exercise has either reps OR time, but not both and not neither
    op.create_check_constraint(
        'ck_session_exercise_one_metric_required',
        'session_exercises',
        'num_nonnulls(reps, time_seconds) = 1'
    )


def downgrade() -> None:
    """Revert schema changes (rollback to reps-only exercises)."""
    
    # Reverse operations in opposite order
    
    # === SESSION_EXERCISES TABLE ===
    
    # Remove new constraints
    op.drop_constraint('ck_session_exercise_one_metric_required', 'session_exercises', type_='check')
    op.drop_constraint('ck_session_exercise_time_positive', 'session_exercises', type_='check')
    op.drop_constraint('ck_session_exercise_reps_positive', 'session_exercises', type_='check')
    
    # Restore old constraint (simple "reps > 0")
    op.create_check_constraint(
        'ck_session_exercise_reps_positive',
        'session_exercises',
        'reps > 0'
    )
    
    # Fill NULL values in reps before making column NOT NULL
    # Using 1 as default to maintain valid data (arbitrary choice)
    op.execute("UPDATE session_exercises SET reps = 1 WHERE reps IS NULL")
    
    # Restore NOT NULL constraint on reps
    op.alter_column('session_exercises', 'reps',
               existing_type=sa.INTEGER(),
               nullable=False)
    
    # Remove time_seconds column
    op.drop_column('session_exercises', 'time_seconds')
    
    # === EXERCISES TABLE ===
    
    # Remove type validation constraint
    op.drop_constraint('ck_exercise_type_valid', 'exercises', type_='check')
    
    # Remove type column
    op.drop_column('exercises', 'type')