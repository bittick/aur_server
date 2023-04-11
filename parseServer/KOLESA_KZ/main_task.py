import requests
import time
from .kolesa_worker import parse_mark
from .marks import MARKS
from loguru import logger


def kolesa_kz_main_cycle():
    req_session = requests.Session()
    for mark_name, mark_id in MARKS.items():
        logger.info(f'processing: {mark_name}')
        start = time.time()
        results = list(parse_mark(mark_id, mark_name, req_session))
        len_res = len(results) if results else None
        logger.info(
            f'parsed: {mark_name}  time: {round(time.time() - start, 2)}  len:{len_res}')
        for i in results:

            if i:
                save_data(i)


def save_data(ad):
    from parseServer.models import CarAd
    CarAd.save_ad(ad)
