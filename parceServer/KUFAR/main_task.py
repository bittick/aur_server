import asyncio
from .kufar_worker import parse_mark
from .marks import MARKS
from loguru import logger


def save_data(ad):
    from parceServer.models_exceptions import AdSetUpError
    from parceServer.models import CarAd
    try:
        CarAd.save_ad(ad)
    except AdSetUpError as e:
        logger.error(f'{e}\n{ad["link"]}')


def kufar_main_cycle():
    for mark_name, mark_id in MARKS.items():
        logger.info(f'processing: {mark_name}')
        parsed_ads = asyncio.run(parse_mark(mark_id, mark_name))
        ln = len(parsed_ads) if parsed_ads else None
        logger.info(f'parced: {mark_name}  len: {ln}')
        if not ln:
            continue
        for i in parsed_ads:
            if i:
                save_data(i)

