"""Add cascade deletes to user-related models

Revision ID: 3675d6a85438
Revises: 4653cf4cd6ae
Create Date: 2025-04-16 19:37:03.491591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3675d6a85438'
down_revision: Union[str, None] = '4653cf4cd6ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('ce_records_ibfk_1', 'ce_records', type_='foreignkey')
    op.create_foreign_key(None, 'ce_records', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('proficiencies_ibfk_1', 'proficiencies', type_='foreignkey')
    op.drop_constraint('proficiencies_ibfk_2', 'proficiencies', type_='foreignkey')
    op.create_foreign_key(None, 'proficiencies', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'proficiencies', 'skills', ['skill_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('shoutouts_ibfk_1', 'shoutouts', type_='foreignkey')
    op.drop_constraint('shoutouts_ibfk_2', 'shoutouts', type_='foreignkey')
    op.create_foreign_key(None, 'shoutouts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'shoutouts', 'users', ['target_user_id'], ['id'], ondelete='SET NULL')
    op.drop_constraint('skills_ibfk_1', 'skills', type_='foreignkey')
    op.create_foreign_key(None, 'skills', 'categories', ['category_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'skills', type_='foreignkey')
    op.create_foreign_key('skills_ibfk_1', 'skills', 'categories', ['category_id'], ['id'])
    op.drop_constraint(None, 'shoutouts', type_='foreignkey')
    op.drop_constraint(None, 'shoutouts', type_='foreignkey')
    op.create_foreign_key('shoutouts_ibfk_2', 'shoutouts', 'users', ['target_user_id'], ['id'])
    op.create_foreign_key('shoutouts_ibfk_1', 'shoutouts', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'proficiencies', type_='foreignkey')
    op.drop_constraint(None, 'proficiencies', type_='foreignkey')
    op.create_foreign_key('proficiencies_ibfk_2', 'proficiencies', 'skills', ['skill_id'], ['id'])
    op.create_foreign_key('proficiencies_ibfk_1', 'proficiencies', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'ce_records', type_='foreignkey')
    op.create_foreign_key('ce_records_ibfk_1', 'ce_records', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
