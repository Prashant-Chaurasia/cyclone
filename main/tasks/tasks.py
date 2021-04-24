from service.server import app, db, celery_app
from .CycloneScrapper import CycloneScrapper

@celery_app.task
def scrape_and_save_data():
    home_page_url = "https://rammb-data.cira.colostate.edu/tc_realtime/"
    scrapper = CycloneScrapper(home_page_url)
    scrapper.process()
    
@celery_app.task
def test_task():
	return True