from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from tokopedia.models import Shop, Good, GoodImage
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
from selenium.common.exceptions import TimeoutException

shop_link = [
    'https://www.tokopedia.com/armiashop'
]

class Command(BaseCommand):
    help = 'sync all goods'

    def __init__(self, stdout = None, stderr = None, no_color = False):
        browser_option = Options()
        browser_option.add_argument('--headless')
        browser_option.add_argument('log-level=3')
        self.browser = webdriver.Chrome(options = browser_option)
        # self.browser.set_page_load_timeout(20)

        super().__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        # cari yang last_update != last_upload dan deskripsinya isi
        pass