"""Add admin user

Revision ID: 1e9e894b5069
Revises: 460da72ba7f4
Create Date: 2021-01-03 18:23:08.644617

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Column, Sequence, Boolean
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import uuid

# revision identifiers, used by Alembic.
revision = '1e9e894b5069'
down_revision = '460da72ba7f4'
branch_labels = None
depends_on = None

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    lms_user = Column(String)
    is_prof = Column(Boolean, default=False)
    token = Column(String, default='')

    def __init__(self, **kwargs):
        kwargs['token'] = str(uuid.uuid4())
        super().__init__(**kwargs)

def upgrade():
    bind = op.get_bind()
    s = Session(bind=bind)

    admin = User(lms_user='admin', is_prof=True)
    print('Admin token:', admin.token)
    s.add(admin)
    s.commit()
    
def downgrade():
    pass
