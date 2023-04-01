import cloudscraper
from parceServer.LIST_AM.parser_1 import parce_mark, MARKS
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
    # price_data = ad.pop('price')
    # if price_data.get('amount'):
    #     if price_data['currency'] == 'USD':
    #         ad['price'] = price_data['amount']
    #     elif price_data['currency'] == 'AMD':
    #         ad['price'] = price_data['amount'] * 0.0026
    #     else:
    #         return  None
    # else:
    #     print('returned NONE')
    #     return None
    # aggregator =Aggregator.objects.filter(name=ad['aggregator'])
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
    #
    # db_ad = CarAd.objects.filter(ad_id=ad['ad_id'])
    # if not db_ad:
    #     db_ad = CarAd.objects.create(**ad)
    # else:
    #     db_ad = db_ad[0]
    #     db_ad.update_object(**ad)
