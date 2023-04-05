def __parse_ad_images(images: list):
    return [i['original_url'] for i in images]


def __parse_ad_parameters(ad_parameters):
    res_params = {}
    for param in ad_parameters:
        param_name = param['name']
        value = param['value']
        match param_name:
            case 'Модель':
                res_params['model'] = value
            case 'Год':
                res_params['production_date'] = value
            case 'Пробег (км.)':
                if not value.isdigit():
                    try:
                        value = value.split(',')[0]
                        res_params['mileage'] = int(value)
                    except ValueError:
                        return None
                else:
                    res_params['mileage'] = int(value)
            case 'Топливо':
                res_params['cars_engine'] = value
            case 'Коробка передач':
                res_params['cars_gearbox'] = value
            case 'Кузов':
                res_params['cars_type'] = value
            case 'Привод':
                res_params['cars_drive'] = value
            case 'Цвет':
                res_params['color'] = value
            case 'Состояние':
                res_params['condition'] = value
            case 'Объем двигателя':
                res_params['engine_capacity'] = value
            # case '':
            #     res_params[''] = value
    return res_params


def parse_data_from_ad(ad, mark_name):
    params = ad.get('params')
    if not params or not ad['price']:
        return None
    res_params = __parse_ad_parameters(params)

    res_params['ad_id'] = ad.get('id')
    res_params['link'] = f"https://lalafo.kg{ad['url']}"
    res_params['price'] = {
        'amount': ad['price'],
        'currency': ad['currency'],
    }
    res_params['title'] = ad['title']
    res_params['description'] = ad['description']
    res_params['country'] = 'Киргизстан'
    res_params['images'] = __parse_ad_images(ad['images'])
    res_params['aggregator'] = 'lalafo.kg'
    res_params['area'] = ad['city']
    res_params['brand'] = mark_name
    return res_params
