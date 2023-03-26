import os
from celery.app.base import Celery as CeleryClass
from celery import Celery
from parceServer.LIST_AM.main_task import do_parsing_cycle

import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurMain.settings')

app = Celery('PARSING')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# def save_data(ad):
#     price_data = ad.pop('price')
#     if price_data.get('value'):
#         # ...
#         ad['price'] = price_data['amount'] * 0.011
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
#         db_ad = CarAd.objects.create(**ad)
#     else:
#         db_ad = db_ad[0]
#         db_ad.update_object(**ad)
#
@app.task()
def test():
    do_parsing_cycle()
    return None


@app.on_after_configure.connect
def setup_periodic_tasks(sender: CeleryClass, **kwargs):
    sender.add_periodic_task(
        datetime.timedelta(minutes=10),
        test.s(),
        start_time=datetime.datetime.now(),
        name='LIST.AM',

    )

#
# setup_periodic_tasks(app)

app.conf.timezone = 'UTC'
