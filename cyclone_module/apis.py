from flask import Blueprint, request, jsonify
from enum import Enum
from http import HTTPStatus
from . import db_utils

cyclone_apis = Blueprint('cyclone_apis', __name__)

@cyclone_apis.route('', methods=['GET'], strict_slashes=False)
def get_all_cyclones():
    cyclones = db_utils.get_all()
    return cyclones, HTTPStatus.OK


@cyclone_apis.route('/<cyclone_id>/forecast_tracks', methods=['GET'], strict_slashes=False)
def get_cyclone_forecast_track(cyclone_id):
    forecast_tracks = db_utils.get_forecast_track_of_cyclone(cyclone_id)
    return forecast_tracks, HTTPStatus.OK


@cyclone_apis.route('/<cyclone_id>/track_historys', methods=['GET'], strict_slashes=False)
def get_cyclone_track_history(cyclone_id):
    track_historys = db_utils.get_track_history_of_cyclone(cyclone_id)
    return track_historys, HTTPStatus.OK