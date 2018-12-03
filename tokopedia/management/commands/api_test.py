from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from selenium.webdriver.support.wait import WebDriverWait

from tokopedia.models import Shop, Good, GoodImage
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import tokopedia.api as toped_api

cookies = ''
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Command(BaseCommand):
    help = 'testing api'

    # def add_arguments(self, parser):
    #     pass

    def get_shop_page(self, link):
        try:
            shop_request = requests.get(link, headers = headers)
            assert shop_request.text.startswith('<!DOCTYPE html>')
            return shop_request.text
        except Exception as e:
            print('get_shop_page', str(e))
        return None


    def shop_reputation(self):
        pass

    def handle(self, *args, **options):
        result = self.get_shop_page('https://www.tokopedia.com/armiashop')
        print(result)