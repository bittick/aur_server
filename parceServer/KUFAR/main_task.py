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

# def save_data_list(ads):
#     from parceServer.models_exceptions import AdSetUpError
#     from parceServer.models import CarAd
#     CarAd.save_ads(ads)
    # try:
    #     CarAd.save_ad(ads)
    # except AdSetUpError as e:
    #     logger.error(f'{e}\n{ads["link"]}')
    # from parceServer.models import Aggregator, CarModel, Brand, CarAd
    # aggregator = Aggregator.objects.filter(name=ad['aggregator'])
    # if not aggregator:
    #     aggregator = Aggregator.objects.create(name=ad['aggregator'])
    # else:
    #     aggregator = aggregator[0]
    # brand = Brand.objects.filter(name=ad['brand'])
    #
    # if not brand:
    #     brand = Brand.objects.create(name=ad['brand'])
    # else:
    #     brand = brand[0]
    # model_name = ad.get('model', 'Другая')
    # model = CarModel.objects.filter(name=model_name)
    # if not model:
    #     model = CarModel.objects.create(name=model_name, brand=brand)
    # else:
    #     model = model[0]
    # ad['aggregator'] = aggregator
    # ad['brand'] = brand
    # ad['model'] = model
    # db_ad = CarAd.objects.filter(ad_id=ad['ad_id'])
    # if not db_ad:
    #     try:
    #         CarAd.objects.create(**ad)
    #     except Exception as e:
    #         logger.error(f'{type(e).__name__} {e}')
    # else:
    #     db_ad = db_ad[0]
    #     db_ad.update_object(**ad)