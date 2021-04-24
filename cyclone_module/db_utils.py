from service.server import db
from models import Cyclone, ForecastTrack, TrackHistory
from libs import serializers
from datetime import datetime
from sqlalchemy.orm import defer
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import insert
import json


def get_by_id(cyclone_id):
    cyclone = Cyclone.query.filter(Cyclone.id == cyclone_id).first()
    return cyclone 

def get_all():
    cyclones = Cyclone.query.all()
    return serializers.serialize({'count': len(cyclones), 'data': cyclones})

def insert_cyclone(region, name, external_id, external_link):
    old_cyclone = old_cyclone = Cyclone.query.filter(Cyclone.external_id == external_id).first()

    if old_cyclone:
        return old_cyclone

    cyclone = Cyclone()
    cyclone.id = cyclone.generate_id()
    cyclone.created_at = datetime.utcnow()

    cyclone.region = region
    cyclone.external_id = external_id
    cyclone.name = name
    cyclone.external_link = external_link

    db.session.add(cyclone)
    db.session.commit()

    return get_by_id(cyclone.id)


def update_object_with_values(obj, values):
    for key, value in values.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
    return obj


def check_and_insert_forecast_tracks(cyclone_id, forecast_at, forecast_tracks):
    ft_list = []
    for forecast_track in forecast_tracks:
        ft = update_object_with_values(ForecastTrack(), forecast_track)
        ft.cyclone_id = cyclone_id
        ft.forecast_at = forecast_at
        ft.created_at = datetime.utcnow()
        ft_list.append(ft.serialize())

    statement = insert(ForecastTrack).values(ft_list).on_conflict_do_nothing()
    db.session.execute(statement)
    db.session.commit()

    return {'Success'}


def check_and_insert_track_historys(cyclone_id, track_historys):
    th_list = []
    for track_history in track_historys:
        th = update_object_with_values(TrackHistory(), track_history)
        th.cyclone_id = cyclone_id
        th.created_at = datetime.utcnow()
        th_list.append(th.serialize())

    statement = insert(TrackHistory).values(th_list).on_conflict_do_nothing()
    db.session.execute(statement)
    db.session.commit()

    return {'Success'}


def get_forecast_track_of_cyclone(cyclone_id):
    forecast_tracks = ForecastTrack.query.filter(ForecastTrack.cyclone_id == cyclone_id).order_by(desc(ForecastTrack.forecast_at)).all()
    return serializers.serialize({'count': len(forecast_tracks), 'data': forecast_tracks})


def get_track_history_of_cyclone(cyclone_id):
    track_historys = TrackHistory.query.filter(TrackHistory.cyclone_id == cyclone_id).order_by(desc(TrackHistory.synoptic_time)).all()
    return serializers.serialize({'count': len(track_historys), 'data': track_historys})

