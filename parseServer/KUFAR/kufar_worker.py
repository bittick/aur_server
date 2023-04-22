import aiohttp
from loguru import logger
from .kufar_ads_tools import parse_ad, find_token, create_params
from bs4 import BeautifulSoup


async def parse_pages(mark, session: aiohttp.ClientSession, model=None, token=None):
    url = 'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated'
    async with session.get(url, params=create_params(mark, model, token)) as resp:
        if resp.status != 200:
            logger.warning(
                f'FAILED REQUEST {resp.url}\n Status code: {resp.status}\n Body: {resp.text}')
            return []
        data = await resp.json()
        # logger.debug(resp.status)
        ads = data.get('ads')
        pagination = data.get('pagination')
        if ads is None:
            return []
        if pagination:
            if len(pagination['pages']) != 1:
                token = find_token(pages=pagination['pages'])
        if token:
            return ads + await parse_pages(mark, session, model, token)
        return ads


async def parse_description(url, session: aiohttp.ClientSession):
    try:
        async with session.get(url) as resp:
            # logger.debug(f'{resp.status} {url}')
            if resp.status != 200:
                if resp.status in ['404', '502']:
                    return await parse_description(url, session)
                return None
            data = await resp.text()
            # soup = BeautifulSoup(data, 'lxml')
            # description = soup.select("div[itemprop='description']")
            # return description[0].text
    except Exception as e:
        logger.error(f'{type(e).__name__} {e}')
        return await parse_description(url, session)


async def parse_mark(mark_id, mark_name):
    async with aiohttp.ClientSession() as session:
        try:
            ads_data = await parse_pages(mark_id, session)
            ads_data = [parse_ad(i, mark_name) for i in ads_data]
            # if ads_data:
            #     urls = [i['link'] for i in ads_data]
            # logger.debug(f'ads count: {len(urls)}')
            tasks = []
            # for url in urls:
            #     tasks.append(asyncio.ensure_future(
            #         parse_description(url, session)))
            # description_data = await asyncio.gather(*tasks)
            # for index, description in enumerate(description_data):
            #     ads_data[index]['description'] = description
            return ads_data
        finally:
            await session.close()
