def __parce_ad_images(images):
    if not images:
        return []
    if images[0]['yams_storage']:
        return [
            f'https://yams.kufar.by/api/v1/kufar-ads/images/{img["id"][:2]}/{img["id"]}.jpg?rule=gallery' for img in
            images
        ]
    else:
        return [
            f'https://rms7.kufar.by/v1/list_thumbs_2x/{img["path"]}' for img in images
        ]


def __parse_ad_parameters(ad_parameters, mark_name):
    res_params = {'brand': mark_name}
    for param in ad_parameters:
        value = param['vl']
        match param['pl']:
            case 'Модель':
                res_params['model'] = value
            case 'Год':
                if value == '1980 или ранее':
                    return None
                res_params['production_date'] = value
            case 'Пробег, км':
                res_params['mileage'] = param['v']
            case 'Тип двигателя':
                res_params['cars_engine'] = value
            case 'Коробка передач':
                res_params['cars_gearbox'] = value
            case 'Тип кузова':
                res_params['cars_type'] = value
            case 'Привод':
                res_params['cars_drive'] = value
            case 'Цвет':
                res_params['color'] = value
            case 'Состояние':
                res_params['condition'] = value
            case 'Объем, л':
                value = value.replace('л', '')
                try:
                    res_params['engine_capacity'] = float(value)
                except ValueError:
                    continue
            case 'Область':
                res_params['region'] = value
            case 'Город / Район':
                res_params['area'] = value
            # case '':
            #     res_params[''] = value
    return res_params


def parse_ad(ad, mark_name):
    res_params = __parse_ad_parameters(ad['ad_parameters'], mark_name)
    if not res_params:
        return None
    res_params['ad_id'] = ad['ad_id']
    res_params['link'] = ad['ad_link']
    res_params['price'] = {
        'amount': float(ad['price_usd']) // 100,
        'currency': 'USD',
    }
    res_params['title'] = ad['subject']
    res_params['country'] = 'Беларусь'
    res_params['images'] = __parce_ad_images(ad['images'])
    res_params['aggregator'] = 'kufar.by'
    return res_params


def create_params(mark, model=None, token=None):
    params = {
        'cat': '2010',
        'cbnd2': mark,
        'cur': 'USD',
        'lang': 'ru',
        'size': '200',
        'sort': 'lst.d',
        'typ': 'sell',
    }
    if model:
        params['cmdl2'] = model
    if token:
        params['cursor'] = token
    return params


def find_token(pages):
    for i in pages:
        if i['label'] == 'next':
            return i['token']
