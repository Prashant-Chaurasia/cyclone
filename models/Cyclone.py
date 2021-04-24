from service.server import db
import datetime
from sqlalchemy import Boolean, Column, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, BYTEA
from libs import helpers


class Cyclone(db.Model):
    __tablename__ = 'cyclones'

    id 	= Column(String(255), primary_key=True)
    created_at = Column(TIMESTAMP)
    external_id = Column(String(255))
    name = Column(String)
    region = Column(String(50))
    external_link = Column(String)
    
    def serialize(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

    def __getitem__(self, item):
        return getattr(self, item)

    def generate_id(self):
        return helpers.generate_id('cy')