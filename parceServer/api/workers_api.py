from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils import json
from ..models import *
from loguru import logger


@api_view(['POST'])
def kufar_ads_process(request):
    ads = json.loads(request.body.decode("utf-8"))
    for ad in ads:
        aggregator = Aggregator.objects.filter(name=ad['aggregator'])
        if not aggregator:
            aggregator = Aggregator.objects.create(name=ad['aggregator'])
        else:
            aggregator = aggregator[0]
        brand = Brand.objects.filter(name=ad['brand'])

        if not brand:
            brand = Brand.objects.create(name=ad['brand'])
        else:
            brand = brand[0]
        model_name = ad.get('model', 'Другая')
        model = CarModel.objects.filter(name=model_name)
        if not model:
            model = CarModel.objects.create(name=model_name, brand=brand)
        else:
            model = model[0]
        ad['aggregator'] = aggregator
        ad['brand'] = brand
        ad['model'] = model
        db_ad = CarAd.objects.filter(ad_id=ad['ad_id'])
        if not db_ad:
            try:
                CarAd.objects.create(**ad)
            except Exception as e:
                logger.error(f'{type(e).__name__} {e}')
        else:
            db_ad = db_ad[0]
            db_ad.update_object(**ad)
    return Response({'Response': 'Ok'}, status=status.HTTP_200_OK)




# @api_view(['POST'])
# def lalafo_ads_process(request):
#     try:
#         ads = json.loads(request.body.decode("utf-8"))
#     except Exception as e:
#         logger.error(f'{type(e).__name__} {e}')
#         print(request.body)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     for ad in ads:
#         try:
#             process_and_save_lalafo_ad(ad)
#         except Exception as e:
#             logger.error(f'{type(e).__name__} {e}')
#             logger.warning(f'ad cannot be saved{e}')
#     return Response({'Response': 'Ok'}, status=status.HTTP_200_OK)
