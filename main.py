#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import pathlib
import time
import lxml.html
import requests


_logger = logging.getLogger(__name__)
_interval = 3.0


def main() -> None:
    max_pages = 23
    for page in range(1, max_pages + 1):
        illust_list(page)


def illust_list(page: int) -> None:
    domain = 'https://prisma-illya.jp'
    url = f'{domain}/portal/illust/page/{page}'
    _logger.info('request %s', url)
    # request
    response = requests.get(url)
    time.sleep(_interval)
    root = lxml.html.fromstring(response.content)
    # illust
    xpath = '//main/section/a'
    for card in root.xpath(xpath):
        illust_url = domain + card.get('href')
        _logger.info('target illust URL: %s', illust_url)
        illust(illust_url)


def illust(url: str) -> None:
    # request
    response = requests.get(url)
    time.sleep(_interval)
    root = lxml.html.fromstring(response.content)
    # parse
    title = root.xpath('//main/article/header/h1')[0].text
    _logger.info('illust title: %s', title)
    illust_url = root.xpath('//main/article/div/img')[0].get('src')
    _logger.info('illust URL %s', illust_url)
    # extension
    extension = illust_url.split('.')[-1]
    _logger.debug('extension: %s', extension)
    # save
    directory = pathlib.Path('illust')
    if not directory.exists():
        directory.mkdir(parents=True)
    illust_path = directory.joinpath(f'{title}.{extension}')
    _logger.info('save to: %s', illust_path.as_posix())
    with illust_path.open(mode='wb') as illust_file:
        # download
        illust_data = requests.get(illust_url)
        time.sleep(_interval)
        illust_file.write(illust_data.content)


if __name__ == '__main__':
    # setup logger
    _logger = logging.getLogger('prisma-illya-illust')
    _logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.formatter = logging.Formatter(
                fmt='%(name)s::%(levelname)s::%(message)s')
    _logger.addHandler(handler)
    # execute main()
    main()
