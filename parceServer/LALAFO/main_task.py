import asyncio
from loguru import logger
from .lalafo_worker import parse_mark
from .marks import MARKS


# def save_ad(ad):
#     from parceServer.models import Aggregator, CarModel, CarAd, Brand
#     price_data = ad.pop('price')
#     if price_data.get('value'):
#         ad['price'] = price_data['value'] * 0.011
#     else:
#         return None
#     aggregator = Aggregator.objects.filter(name=ad['aggregator'])
#     if not aggregator:
#         aggregator = Aggregator.objects.create(name=ad['aggregator'])
#     else:
#         aggregator = aggregator[0]
#     brand = Brand.objects.filter(name=ad['brand'])
#
#     if not brand:
#         brand = Brand.objects.create(name=ad['brand'])
#     else:
#         brand = brand[0]
#     model_name = ad.get('model', 'Другая')
#     model = CarModel.objects.filter(name=model_name)
#     if not model:
#         model = CarModel.objects.create(name=model_name, brand=brand)
#     else:
#         model = model[0]
#     ad['aggregator'] = aggregator
#     ad['brand'] = brand
#     ad['model'] = model
#
#     db_ad = CarAd.objects.filter(ad_id=ad['ad_id'])
#     if not db_ad:
#         CarAd.objects.create(**ad)
#     else:
#         db_ad = db_ad[0]
#         db_ad.update_object(**ad)
def save_data(ad):
    from parceServer.models_exceptions import AdSetUpError
    from parceServer.models import CarAd
    try:
        CarAd.save_ad(ad)
    except AdSetUpError as e:
        logger.error(f'{e}\n{ad["link"]}')
    except Exception:
        print(ad)
        raise Exception

def lalafo_main_cycle():
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

        # data = await asyncio.gather(*tasks)
        # return [j for i in data for j in i]
