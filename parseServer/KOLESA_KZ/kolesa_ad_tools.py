import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import re
from loguru import logger


def __parse_raw_params(raw_params: dict):
    res = {}
    for name, value in raw_params.items():
        match name:
            case 'Город':
                res['region'] = value
            case 'Поколение':
                res['generation'] = value
            case 'Кузов':
                res['cars_type'] = value
            case 'Объем двигателя, л':
                tmp = re.sub('[\s+| ) ]', '', value).split('(')
                res['engine_capacity'] = tmp[0]
                res['cars_engine'] = tmp[1]
            case 'Пробег':
                res['mileage'] = int(re.sub(r'\D+', '', value))
            case 'Коробка передач':
                res['cars_gearbox'] = value
            case 'Привод':
                res['cars_drive'] = value
    return res


def __parse_images(photo_gallery: Tag):
    res = []
    for i in photo_gallery.contents:
        if isinstance(i, Tag):
            res.append(
                re.sub('full.webp', '750x470.webp', i.button['data-href']))
    return res


def __parse_params(parametrs_html):
    raw_params = {}
    for i in parametrs_html:
        if isinstance(i, Tag):
            raw_params[i.contents[1]['title']] = i.contents[3].text
    return __parse_raw_params(raw_params)


def __parse_price(raw_price):
    return int(re.sub(r"[\xa0 | \n | ₸ | ]", "", raw_price))


def __parse_description(raw_descr):
    return re.sub(r'\s+', ' ', raw_descr)


def parse_one_html(html_content, mark_name, link):
    try:
        soup = BeautifulSoup(html_content, 'lxml')
        parametrs_html = soup.find('div', {'class': 'offer__parameters'}).children
        params = __parse_params(parametrs_html)
        title_tag = soup.find('h1', {'class': 'offer__title'})
        title_data = list(filter(lambda x: isinstance(x, Tag), title_tag.contents))
        title_data = [i.text for i in title_data]
        _, model, year, _ = title_data
        title_data[0] = title_data[0] + ' '
        params['country'] = 'Казахстан'
        params['aggregator'] = 'kolesa.kz'
        params['brand'] = mark_name
        params['model'] = model[:-1]
        params['condition'] = 'Б/у'
        params['production_date'] = int(year)
        params['title'] = ''.join(title_data)
        params['ad_id'] = link[8:17]
        params['link'] = f'https://kolesa.kz{link}'
        try:
            raw_descr = soup.find('div', {'class': 'offer__description'}).div.p.text
            params['description'] = __parse_description(raw_descr)
        except AttributeError:
            pass
        raw_price = soup.find('div', {'class': 'offer__price'}).text
        photo_gallery = soup.find('ul', {'class': 'gallery__thumbs-list'})
        params['price'] = {'amount': __parse_price(raw_price),
                           'currency': 'KZT'}

        params['images'] = __parse_images(photo_gallery)
        return params
    except Exception as e:
        logger.error(e)
