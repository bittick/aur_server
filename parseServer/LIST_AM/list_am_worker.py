from .list_am_ads_tools import parse_one_ad, parse_urls_from_page
import cloudscraper
from concurrent.futures import ThreadPoolExecutor
from loguru import logger


def create_mark_link(mark_id: int | str, page: int | str = 1) -> str:
    if page == 1:
        return f'https://www.list.am/ru/category/23?n=0&bid={mark_id}&crc=-1&srt=3'
    else:
        return f'https://www.list.am/ru/category/23/{page}?n=0&bid={mark_id}&crc=-1&srt=3'


def get_ads_links(mark_id, session: cloudscraper.CloudScraper, limit=30) -> list[str] | None:
    try:
        resp = session.get(url=create_mark_link(mark_id))
    except Exception as e:
        logger.error(e)
        return None
    page_counter = 1
    ads_urls, next_page = parse_urls_from_page(resp.content)
    while next_page and page_counter < limit:
        page_counter += 1
        new_url = create_mark_link(mark_id, page_counter)
        resp = session.get(new_url)
        other_urls, next_page = parse_urls_from_page(resp.content)
        ads_urls += other_urls
    return ads_urls


def parse_one_ad_link(args: list[str | cloudscraper.CloudScraper]) -> dict | None:
    ad_url, session = args
    try:
        resp = session.get(f'https://www.list.am{ad_url}')
        # logger.info(f'{resp.url} {resp.status_code}')
        ad_params = parse_one_ad(resp.content, resp.url)
    except Exception as e:
        logger.error(e)
        return None
    return ad_params


def parse_mark(mark_id: int | str, session: cloudscraper.CloudScraper) -> list[dict | None]:
    res = get_ads_links(mark_id, session, 10)
    if res:
        args = [(i, session) for i in res]
        with ThreadPoolExecutor(max_workers=10) as executor:
            res = executor.map(parse_one_ad_link, args)
            return list(res)
    else:
        return []
