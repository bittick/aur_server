from typing import Any
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import re


def parse_urls_from_page(html: str | bytes) -> (list[str] | str | None):
    soup = BeautifulSoup(html, 'lxml')
    galery: list[Tag] = soup.find_all('div', {'class': 'gl'})
    galery_index = 0 if len(galery) == 1 else 1
    urls = []
    if galery:
        for i in galery[galery_index].contents:
            urls.append(i['href'])
    pages = soup.find('div', {'class': 'dlf'})
    next_page = None
    if pages:
        if isinstance(pages.contents[-1], Tag):
            next_page = pages.contents[-1]['href']
    return urls, next_page


def _switch_attrs(attrs: Tag) -> dict:
    res = {}
    for i in attrs.contents:
        tags = i.contents
        name, value = tags[0].text, tags[1].text
        match name:
            case 'Марка':
                res['brand'] = value
            case 'Модель':
                res['model'] = value
            case 'Тип кузова':
                res['cars_type'] = value
            case 'Год':
                res['production_date'] = value
            case 'Тип двигателя':
                res['cars_engine'] = value
            case 'Коробка передач':
                res['cars_gearbox'] = value
            case 'Привод':
                res['cars_drive'] = value
            case 'Объём двигателя':
                res['engine_capacity'] = float(re.sub('[L]', '', value))
    return res


def _switch_info(info: Tag) -> dict:
    res = {}
    for i in info.contents:
        tags = i.contents
        name, value = tags[0].text, tags[1].text
        match name:
            case 'Пробег':
                if 'миль' in value:
                    miles = int(re.sub('[,|миль]', '', value))
                    res['mileage'] = round(miles * 1.6)
                else:
                    res['mileage'] = int(re.sub('[,|км]', '', value))
            case 'Состояние':
                res['condition'] = value
    return res


def _get_color(exterior: Tag) -> str:
    res = {}
    for i in exterior.contents:
        tags = i.contents
        name, value = tags[0].text, tags[1].text
        match name:
            case 'Цвет кузова':
                return value


def _parse_price(price_tag: Tag) -> dict[str, float | Any]:
    if price_tag:
        currency = price_tag.contents[1]["content"]
        return {
            'amount': float(price_tag['content']),
            'currency': currency
        }


def _parse_description(description: Tag) -> str:
    res = []
    for i in description.contents:
        if isinstance(i, NavigableString):
            res.append(i.text)
        else:
            res.append('\n')
    return ''.join(res)


def parse_one_ad(html: str | bytes, link: str) -> dict | None:
    soup = BeautifulSoup(html, 'lxml')
    try:
        blocks = soup.findAll('div', {'class': 'attr g'})[:3]
        attrs, info, exterior = blocks
    except ValueError as e:
        pass
        # logger.warning(f'{link} not enough information ')
        # logger.warning(e)
        return None
    params = _switch_attrs(attrs)
    params['ad_id'] = re.sub('[https://www.list.am/ru/item/]', '', link)
    params['aggregator'] = 'list.am'
    params['country'] = 'Армения'
    params['link'] = link
    address = soup.find('div', {'class': 'loc'})
    if address:
        address = address.text.split(' › ')
        if len(address) == 2:
            params['region'], params['area'] = address
        else:
            params['region'] = address[0]
    color = _get_color(exterior)
    if color:
        params['color'] = color
    params['title'] = soup.find('h1', {'itemprop': 'name'}).text
    price = _parse_price(soup.find('span', {'class': 'price'}))
    if not price:
        return None
    params['price'] = price
    params.update(**_switch_info(info))
    params['description'] = _parse_description(
        soup.find('div', {'itemprop': 'description'}))
    galery = str(soup.findAll('script'))
    images = list(map(lambda a: 'https:' + a, re.findall(
        "(//s\.[^\"\s]+)", galery)))
    params['images'] = images
    return params
