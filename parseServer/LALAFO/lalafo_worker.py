import aiohttp
import asyncio

from aiohttp import ClientPayloadError

from .header import HEADER
from loguru import logger
from .lalafo_ads_tools import parse_data_from_ad


def create_params(mark_id, page=2):
    return {
        'expand': 'url',
        'per-page': '500',
        'category_id': f'{mark_id}',
        'sort_by': '-price',
        'page': f'{page}',
    }


def parse_ids_from_page(json):
    items = json['items']
    return [i['id'] for i in items]


async def parse_count(mark, session):
    try:
        async with session.get(f'https://lalafo.kg/api/search/v3/feed/count?category_id={mark}',
                               headers=HEADER) as resp:
            if resp.status == 200:
                data = await resp.json()
                return int(data['ads_count'])
    except Exception as e:
        logger.error(e)


async def parse_ids(mark, session: aiohttp.ClientSession, pages=1):
    tasks = []
    for page in range(pages):
        tasks.append(asyncio.ensure_future(
            parse_ids_from_one_page(mark, session, page)))
    data = await asyncio.gather(*tasks)
    res = []
    for i in data:
        if i:
            res = res + i
    return list(set(res))


async def parse_ids_from_one_page(mark, session: aiohttp.ClientSession, page=1):
    try:
        async with session.get('https://lalafo.kg/api/search/v3/feed/search', params=create_params(mark, page),
                               headers=HEADER) as resp:
            if resp.status == 200:
                return parse_ids_from_page(await resp.json())
    except ClientPayloadError as e:
        logger.error(e)


async def parse_one_ad(session: aiohttp.ClientSession, ad_id):
    try:
        async with session.get(f'https://lalafo.kg/api/search/v3/feed/details/{ad_id}?expand=url', headers=HEADER) \
                as resp:
            if resp.status == 200:
                data = await resp.json()
                # logger.info(f'id:{id} status:{resp.status}')
                return data
    except Exception as e:
        logger.error(f'id:{ad_id} error:{e}')


async def parse_ads(ids, session: aiohttp.ClientSession):
    tasks = []
    for ad_id in ids:
        tasks.append(asyncio.ensure_future(parse_one_ad(session, ad_id)))

    data = await asyncio.gather(*tasks)
    return [i for i in data if i]


async def parse_mark(mark_id, mark_name):
    async with aiohttp.ClientSession() as session:
        try:
            count = await parse_count(mark_id, session)
            if not count:
                pages = 0
            else:
                pages = count // 500 + 2 if count % 500 != 0 else count // 500 + 1
            ids = await parse_ids(mark_id, session, pages)
            raw_ads = await parse_ads(ids, session)
            if raw_ads:
                ads = []
                for i in raw_ads:
                    parsed_data = parse_data_from_ad(i, mark_name)
                    if parsed_data:
                        ads.append(parsed_data)
                return ads
        finally:
            await session.close()
