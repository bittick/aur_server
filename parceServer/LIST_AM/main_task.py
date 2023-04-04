import cloudscraper
from .list_am_worker import parce_mark
from .marks import MARKS
from loguru import logger
import time


def list_am_main_cycle():
    scraper_session = cloudscraper.CloudScraper()
    for mark_name, mark_id in MARKS.items():
        logger.info(f'processing: {mark_name}')
        start = time.time()
        results = parce_mark(mark_id, scraper_session)
        logger.info(
            f'parsed: {mark_name}  time: {round(time.time() - start, 2)}  len:{len(results)}')
        for i in results:

            if i:
                save_data(i)


def save_data(ad):
    from parceServer.models import CarAd
    CarAd.save_ad(ad)
