import logging
import re

import requests
from bs4 import BeautifulSoup
from logging import getLogger

_module_name = 'parsers'


def get_parser(url):
    response = requests.get(url)
    text = response.text
    return BeautifulSoup(text, "html.parser")


time_re = re.compile(r'\d{2}:\d{2}')
def strip_time(time_str):
    if found := time_re.search(time_str):
        return found.group() if found else None


class Parser:
    url: str
    p: BeautifulSoup

    def __init__(self, url):
        self.url = url
        self.p = get_parser(url)

    def parse(self, *args, **kwargs):
        logging.info(f'call {self.__class__.__name__} with url "{self.url}"')
        return self._parse_internal(*args, **kwargs)

    def _parse_internal(self, *args, **kwargs):
        pass
