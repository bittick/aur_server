import time
import requests
from .kolesa_ads_tools import parse_one_html
from bs4 import BeautifulSoup
from bs4.element import Tag
from loguru import logger
from .connect_vars import PROXY, TIMEOUT, REFRESH_LINK, PAGE_LIMIT
from concurrent.futures import ThreadPoolExecutor
import threading

refresh_mutex = threading.Lock()


def proxy_request(session: requests.Session):
    request_success = False
    r = None
    while not request_success:
        try:
            r = session.get(REFRESH_LINK, timeout=8)
            return r.status_code
        except requests.exceptions.Timeout:
            time.sleep(3)
            pass
    return r


def refresh_proxy(session: requests.Session):
    global refresh_mutex
    # Пытаемся захватить мьютекс
    if refresh_mutex.acquire(blocking=False):
        logger.debug('trying to refresh proxy')
        proxy_request(session)
        threading.Timer(10, refresh_mutex.release).start()
    else:
        # Мьютекс уже занят, ждем его освобождения
        time.sleep(3)
        return None


def parse_links_from_one_page(args):
    mark, number, session = args
    url = f'https://kolesa.kz{mark}'
    params = {'page': number,
              'sort_by': 'add_date-asc'} if number != 1 else {'sort_by': 'add_date-asc'}
    try:
        resp = session.get(url, params=params, headers={
            'user-agent': 'Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00'}, proxies=PROXY,
                           timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        # logger.error(e)
        status = refresh_proxy(session)
        if status:
            logger.debug(f'REFRESHING PROXY: status - {status}')
        return parse_links_from_one_page((mark, number, session))
    logger.debug(resp.url)
    if resp.status_code == 200:
        data = resp.content
        soup = BeautifulSoup(data, 'html.parser')
        find_res = soup.find_all('div', {'class': 'a-list'})
        if not find_res:
            return None
        data: Tag = find_res[0]
        h5_title: list[Tag] = data.find_all(
            'h5', {'class': 'a-card__title'})
        links = [i.findChildren("a", recursive=False)[
                     0]['href'] for i in h5_title]
        return links


def pase_ads_links(mark: str, count: str | int, session: requests.Session, limit=PAGE_LIMIT):
    res = []
    if count > limit:
        count = limit

    args = [(mark, i + 1, session) for i in range(count)]
    with ThreadPoolExecutor(max_workers=10) as executor:
        liks_data = executor.map(parse_links_from_one_page, args)
        res = []
        for i in liks_data:
            res += i
        return res


def get_one_ad(ad_link, session: requests.Session):
    request_success = False
    r = None
    while not request_success:
        try:
            url = f'http://kolesa.kz{ad_link}'
            r = session.get(url, proxies=PROXY, timeout=TIMEOUT)
            if r.status_code == 200:
                request_success = True
                logger.debug(f'{r.url} {r.status_code}')
                return r.text
            logger.warning(f'{r.url} {r.status_code}')
            raise requests.exceptions.RequestException()
        except requests.exceptions.RequestException as e:
            status = refresh_proxy(session)
            if status:
                logger.debug(f'REFRESHING PROXY: status - {status}')
    return r


def parse_one_ad(args):
    link, mark_name, session = args
    html = get_one_ad(link, session)
    data = parse_one_html(html, mark_name, link)
    if data:
        return data


def get_mark_page_count(mark, session: requests.Session):
    header = {
        'authority': 'kolesa.kz',
        'method': 'GET',
        'accept': 'application/json, text/plain, */*',
        'x-requested-with': 'XMLHttpRequest',
    }
    url = f'https://kolesa.kz/a/ajax-get-search-nb-results{mark}'
    try:
        resp = session.get(url, headers=header, proxies=PROXY, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        status = refresh_proxy(session)
        if status:
            logger.debug(f'REFRESHING PROXY: status - {status}')
        return get_mark_page_count(mark, session)
    data = resp.json()
    ads_count = data['nbCnt']
    count = ads_count // 20 if ads_count % 20 == 0 else ads_count // 20 + 1
    return count


def parse_mark(mark, mark_name, session: requests.Session):
    count = get_mark_page_count(mark, session)
    links = pase_ads_links(mark, count, session)
    logger.debug(links)
    args = [(i, mark_name, session) for i in links]
    with ThreadPoolExecutor(max_workers=10) as executor:
        return executor.map(parse_one_ad, args)


if __name__ == '__main__':
    session = requests.Session()
    data = parse_mark('/cars/audi/', 'Audi', session)
    data = list(filter(lambda x: x is not None, data))
    f = open('data.json', 'w')
    import json

    json.dump(data, f, ensure_ascii=False, indent=4)
