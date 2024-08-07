"""Add

Revision ID: 1e4fe47b6727
Revises: 
Create Date: 2024-07-09 09:35:49.905996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e4fe47b6727'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("company", sa.String(length=50), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('assemble_delivery_fees',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('second_name', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sku',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sku_name', sa.String(length=50), nullable=False),
    sa.Column('height', sa.Float(), nullable=False),
    sa.Column('length', sa.Float(), nullable=False),
    sa.Column('width', sa.Float(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sku_name')
    )
    op.create_table('ahs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('ahs_type', sa.Enum('AHS_Dimension', 'AHS_Weight', 'AHS_Packing', name='ahstype'), nullable=False),
    sa.Column('gd_hd_type', sa.Enum('GROUND', 'HOMEDELIVERY', name='gdandhd'), nullable=False),
    sa.Column('res_comm_type', sa.Enum('RESIDENTIAL', 'COMMERCIAL', name='resandcomm'), nullable=False),
    sa.Column('fees', sa.Float(), nullable=False),
    sa.Column('delivery_version_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['delivery_version_id'], ['assemble_delivery_fees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('base_rate',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('rate_weight', sa.Integer(), nullable=False),
    sa.Column('zone', sa.Integer(), nullable=False),
    sa.Column('fees', sa.Float(), nullable=False),
    sa.Column('delivery_version_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['delivery_version_id'], ['assemble_delivery_fees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('das',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('das_type', sa.Enum('DAS', 'DASE', 'RAS', name='dastype'), nullable=False),
    sa.Column('gd_hd_type', sa.Enum('GROUND', 'HOMEDELIVERY', name='gdandhd'), nullable=False),
    sa.Column('res_comm_type', sa.Enum('RESIDENTIAL', 'COMMERCIAL', name='resandcomm'), nullable=False),
    sa.Column('fees', sa.Float(), nullable=False),
    sa.Column('delivery_version_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['delivery_version_id'], ['assemble_delivery_fees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('oversize',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('gd_hd_type', sa.Enum('GROUND', 'HOMEDELIVERY', name='gdandhd'), nullable=False),
    sa.Column('fees', sa.Float(), nullable=False),
    sa.Column('delivery_version_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['delivery_version_id'], ['assemble_delivery_fees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rdc',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('gd_hd_type', sa.Enum('GROUND', 'HOMEDELIVERY', name='gdandhd'), nullable=False),
    sa.Column('fees', sa.Float(), nullable=False),
    sa.Column('delivery_version_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['delivery_version_id'], ['assemble_delivery_fees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rdc')
    op.drop_table('oversize')
    op.drop_table('das')
    op.drop_table('base_rate')
    op.drop_table('ahs')
    op.drop_table('sku')
    op.drop_table('assemble_delivery_fees')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
