from service.server import app, db, celery_app
from bs4 import BeautifulSoup
from main.cyclone_module import db_utils
from main.libs import helpers
import re
import requests

class CycloneScrapper:

    def __init__(self, start_url):
        self.start_url = start_url


    def save_cyclone_info(self, region, detail_link):
        external_id, name = detail_link.text.strip().split(' - ')
        if external_id:
            external_link = self.start_url + detail_link['href']
            cyclone = db_utils.insert_cyclone(region = region, name = name, external_id = external_id, external_link = external_link)
            return cyclone
        return None


    def find_and_save_cylone_info(self, soup):
        current_cyclones = []
        
        for cyclone_html in soup.findAll('div', attrs={'class':'basin_storms'}):
            region = cyclone_html.find('h3').text
            cyclone_detail_links = cyclone_html.findAll('a')
            
            for detail_link in cyclone_detail_links:
                cyclone = self.save_cyclone_info(region, detail_link)
                
                if cyclone:
                    current_cyclones.append(cyclone)
        return current_cyclones


    def generate_forecast_tracks(self, forecast_table):
        forecast_tracks = []
        for row in forecast_table.find_all('tr')[1:]:
            columns = row.find_all('td')

            keys = ['forecast_hour', 'latitude', 'longitude', 'intensity']
            forecast_track = {}
            for index, column in enumerate(columns):
                forecast_track[keys[index]] = column.get_text()

            forecast_tracks.append(forecast_track)
        return forecast_tracks


    def get_forecast_time(self, soup):
        forcast_time_tag = soup.find('h4', string=re.compile('Time of Latest Forecast.*'))
        forcast_time_str = re.compile(': ').split(forcast_time_tag.text)[1]
        forcast_time = helpers.parse_datetime(forcast_time_str)
        return forcast_time


    def generate_track_historys(self, track_history_table):
        track_historys = []
        for row in track_history_table.find_all('tr')[1:]:
            columns = row.find_all('td')

            keys = ['synoptic_time', 'latitude', 'longitude', 'intensity']
            track_history = {}
            for index, column in enumerate(columns):
                value = column.get_text()
                if index == 0:
                    # converting synoptic_time to datetime
                    value = helpers.parse_datetime(value)
                
                track_history[keys[index]] = value
            track_historys.append(track_history)
        return track_historys


    def process_cyclone(self, cyclone):
        cyclone_info_page = requests.get(cyclone.external_link)
        soup = BeautifulSoup(cyclone_info_page.text, 'html.parser')
        tables = soup.findAll('table')

        if tables:
            # Forecast tracks - only if the info is avalaible then we can save in the db
            if (soup.find('h4', string=re.compile('Time of Latest Forecast.*')) and len(tables) == 2):
                forecast_tracks = self.generate_forecast_tracks(tables[0])
                forcast_time = self.get_forecast_time(soup)
                db_utils.check_and_insert_forecast_tracks(cyclone.id, forcast_time, forecast_tracks)
        
            # Track history - 
            track_history_table = tables[0] if len(tables) == 1 else tables[1]
            track_historys = self.generate_track_historys(track_history_table)
            db_utils.check_and_insert_track_historys(cyclone.id, track_historys)


    def process(self):
        mainpage = requests.get(self.start_url)
        soup = BeautifulSoup(mainpage.text, 'html.parser')
        current_cyclones = self.find_and_save_cylone_info(soup)

        for cyclone in current_cyclones:
            self.process_cyclone(cyclone)


