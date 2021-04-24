from service.server import app, db
import json
import pytest
from main.libs import helpers, serializers
from main.tasks.CycloneScrapper import CycloneScrapper
from main.tasks.tasks import test_task
from main.models import Cyclone, ForecastTrack, TrackHistory
from bs4 import BeautifulSoup
from datetime import datetime


@pytest.fixture
def client():
    return app.test_client()

def test_service_ready(client):
    res = client.get('/ready')
    assert res.status_code == 200
    expected = {"message": "Service is ready!"}
    assert expected == json.loads(res.get_data(as_text=True))


def test_db_connections(client):
    cyclones = db.session.query(Cyclone).all()


def test_celery_worker_redis(client):
    resp = test_task.apply().get()
    assert resp


def test_generate_id(client):
    id = helpers.generate_id('cy')
    assert len(id) == 12


def test_parse_datetime(client):
    parsed_dt = helpers.parse_datetime("2021-04-24 00:00")
    assert isinstance(parsed_dt, datetime)


def test_generate_forecast_track(client):
    test_html = "<table> <tbody>\
        <tr>\
            <td>Forecast Hour</td>\
            <td>Latitude</td>\
            <td>Longitude</td>\
            <td>Intensity</td>\
        </tr>\
        <tr>\
            <td>0</td>\
            <td>23.0</td>\
            <td>131.1</td>\
            <td>55</td>\
        </tr>\
    </tbody></table>"
    test_url = "http://google.com"
    scrapper = CycloneScrapper(test_url)

    ft_tracks = scrapper.generate_forecast_tracks(BeautifulSoup(test_html, 'html.parser'))
    assert len(ft_tracks) == 1
    assert ft_tracks[0]['forecast_hour'] == '0'


def test_generate_track_history(client):
    test_html = "<table> <tbody>\
        <tr>\
            <td>Synoptic Time</td>\
            <td>Latitude</td>\
            <td>Longitude</td>\
            <td>Intensity</td>\
        </tr>\
        <tr>\
            <td>2021-04-24 00:00</td>\
            <td>23.0</td>\
            <td>131.1</td>\
            <td>55</td>\
        </tr>\
    </tbody></table>"
    test_url = "http://google.com"
    scrapper = CycloneScrapper(test_url)

    track_historys = scrapper.generate_track_historys(BeautifulSoup(test_html, 'html.parser'))
    assert len(track_historys) == 1
    assert isinstance(track_historys[0]['synoptic_time'], datetime)


def test_cyclone_object_initialisation(client):
    cyclone = Cyclone(id = 'cy123', external_id = 'sg123', name = 'Test', region = 'Atlantic', 
                    external_link = 'http://localhost:1234')

    assert isinstance(cyclone, Cyclone)


def test_forecast_track_object_initialisation(client):
    forecast_track = ForecastTrack(id = '1', cyclone_id = 'cy123', forecast_at = datetime.utcnow(), forecast_hour = '12', latitude = -4, 
                    longitude = -12.5, intensity = 35)

    assert isinstance(forecast_track, ForecastTrack)


def test_track_history_object_initialisation(client):
    track_history = TrackHistory(id = '1', cyclone_id = 'cy123', synoptic_time = datetime.utcnow(), latitude = -4, 
                    longitude = -12.5, intensity = 35)

    assert isinstance(track_history, TrackHistory)


def test_get_cyclones(client):
    res = client.get('/cyclones')
    assert res.status_code == 200


def test_get_forecast_tracks(client):
    res = client.get('/cyclones/random_id/forecast_tracks')
    assert res.status_code == 200


def test_get_track_history(client):
    res = client.get('/cyclones/random_id/track_historys')
    assert res.status_code == 200