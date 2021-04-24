from service.server import db
import datetime
from sqlalchemy import Boolean, Column, Numeric, String, BigInteger
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, BYTEA

class TrackHistory(db.Model):
    __tablename__ = 'track_historys'
    
    id  = Column(BigInteger, primary_key=True)
    cyclone_id 	= Column(String(255))
    created_at = Column(TIMESTAMP)
    synoptic_time = Column(TIMESTAMP)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    intensity = Column(Numeric)
    
    def serialize(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

    def __getitem__(self, item):
        return getattr(self, item)