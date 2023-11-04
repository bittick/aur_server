import cloudscraper
from .list_am_worker import parse_mark
from .marks import MARKS
from loguru import logger
import time


def list_am_main_cycle():
    scraper_session = cloudscraper.CloudScraper()
    try:
        for mark_name, mark_id in MARKS.items():
            logger.info(f'processing: {mark_name}')
            start = time.time()
            results = parse_mark(mark_id, scraper_session)
            logger.info(
                f'parsed: {mark_name}  time: {round(time.time() - start, 2)}  len:{len(results) if results else 0}')
            for i in results:

                if i:
                    save_data(i)
    finally:
        scraper_session.close()


def save_data(ad):
    from parseServer.models import CarAd
    try:
        CarAd.save_ad(ad)
    except Exception as e:
        logger.error(e)
