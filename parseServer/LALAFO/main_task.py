import asyncio
import time
from loguru import logger
from .lalafo_worker import parse_mark
from .marks import MARKS


def save_data(ad):
    from parseServer.models_exceptions import AdSetUpError
    from parseServer.models import CarAd
    try:
        CarAd.save_ad(ad)
    except AdSetUpError as e:
        logger.error(f'{e}\n{ad["link"]}')
    except Exception as e:
        logger.error(f'{e}\n{ad["link"]}')


def lalafo_main_cycle():
    for mark_name, mark_id in MARKS.items():
        logger.info(f'processing: {mark_name}')
        start = time.time()
        parsed_ads = asyncio.run(parse_mark(mark_id, mark_name))
        ads_len = len(parsed_ads) if parsed_ads else None
        logger.info(
            f'parsed: {mark_name}  time: {round(time.time() - start, 2)}  len:{ads_len}')
        if not ads_len:
            continue
        for i in parsed_ads:
            if i:
                save_data(i)
