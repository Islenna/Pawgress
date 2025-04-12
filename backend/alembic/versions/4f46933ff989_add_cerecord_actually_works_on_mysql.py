"""Add CERecord (actually works on MySQL)

Revision ID: 4f46933ff989
Revises: 620f9354de50
Create Date: 2025-04-12 15:23:10.240920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f46933ff989'
down_revision: Union[str, None] = '620f9354de50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ce_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('ce_type', sa.Text(), nullable=False),
    sa.Column('ce_description', sa.Text(), nullable=False),
    sa.Column('ce_date', sa.Date(), nullable=False),
    sa.Column('ce_hours', sa.Float(), nullable=False),
    sa.Column('ce_file_path', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ce_records_id'), 'ce_records', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ce_records_id'), table_name='ce_records')
    op.drop_table('ce_records')
    # ### end Alembic commands ###
