"""empty message

Revision ID: 49d5b06dce08
Revises: 
Create Date: 2023-09-22 13:20:45.641460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49d5b06dce08'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('motto', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('_password_hash', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('co_mingle', sa.Boolean(), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], name=op.f('fk_events_organization_id_organizations')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], name=op.f('fk_user_organizations_organization_id_organizations')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_organizations_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_organizations')
    op.drop_table('events')
    op.drop_table('users')
    op.drop_table('organizations')
    # ### end Alembic commands ###
