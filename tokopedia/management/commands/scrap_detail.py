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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

shop_link = [
    'https://www.tokopedia.com/armiashop'
]

def information_loaded(driver):
    try:
        element_view = driver.find_element_by_xpath("//div[@class='rvm-product-info']//div[@class='inline-block va-middle']//div[@class='rvm-product-info--item_value mt-5 view-count']")
        element_sold = driver.find_element_by_xpath("//div[@class='rvm-product-info']//div[@class='inline-block va-middle']//div[@class='rvm-product-info--item_value mt-5 item-sold-count']")
    except NoSuchElementException:
        return False
    return (not element_view.text.startswith(' ') and not element_sold.text.startswith(' '))

class Command(BaseCommand):
    help = 'scrap all good\'s missing detail'

    def __init__(self, stdout = None, stderr = None, no_color = False):
        browser_option = Options()
        browser_option.add_argument('--headless')
        browser_option.add_argument('log-level=3')
        browser_option.add_experimental_option("prefs", {
            'profile.managed_default_content_settings.images': 2,
            'disk-cache-size': 4096
        })

        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"

        self.browser = webdriver.Chrome(
            options = browser_option,
            desired_capabilities = desired_capabilities
            )
        # self.browser.set_page_load_timeout(15)
        self.wait = WebDriverWait(self.browser, 500)

        super().__init__(stdout, stderr, no_color)

    def handle(self, *args, **options):
        # self.scrap_goods_detail()
        self.scrap_goods_detail_without_aggregate()

    def scrap_goods_detail_without_aggregate(self):
        unfinished_goods = Good.objects.filter(informasi_produk = None)
        goods_amount = len(unfinished_goods)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        i = 1
        for good in unfinished_goods:
            print('\t[' + str(i) + '/' + str(goods_amount) + '] [SCRAPPING GOODS DETAIL]', good.nama_barang)

            result = ''
            try:
                result = requests.get(good.link_barang, headers = headers, timeout = 20)
            except Exception as e:
                print('\t' + str(e))
                continue


            instance = BeautifulSoup(result.text, 'html.parser')
            # html_parrent_info = instance.find('div', {'class': 'rvm-product-info'})
            # item_view = html_parrent_info.find('div', {'class': 'view-count'})
            # item_sold = html_parrent_info.find('div', {'class': 'item-sold-count'})

            html_sumary = instance.find('div', {'class': 'product-summary__content'})

            summary_raw_text = str(html_sumary)
            summary_removed_br = summary_raw_text.replace('<br/>', '[ENDLINE]')
            temp_instance = BeautifulSoup(summary_removed_br, 'html.parser')
            removed_multispace = re.sub('\ +', ' ', temp_instance.text.strip())
            removed_endline = removed_multispace.replace('\n', '')
            generate_new_endline = removed_endline.replace('[ENDLINE]', '\n')
            removed_outlier_space = generate_new_endline.replace('\n ', '\n')
            item_summary = removed_outlier_space

            images = instance.find_all('div', {'class': 'content-img-relative'})
            for image in images:
                image_link = image.img['src']
                GoodImage.objects.get_or_create(
                    link_gambar = image_link,
                    defaults = {
                        'barang_induk': good,
                    }
                )

            # good.dilihat = item_view.text
            # good.terjual = item_sold.text
            good.informasi_produk = item_summary
            good.last_update = timezone.now()
            good.save()
            i += 1


    # todo: make unitest
    def scrap_goods_detail(self):
        unfinished_goods = Good.objects.filter(informasi_produk = None)
        goods_amount = len(unfinished_goods)

        # via selenium headless
        i = 1
        for good in unfinished_goods:
            print('\t[' + str(i) + '/' + str(goods_amount) + '] Scrapping detail of', good.nama_barang)

            try:
                self.browser.get(good.link_barang)
                self.wait.until(information_loaded)
            except TimeoutException as e:
                print('\ttimeout exception')
            finally:
                html = self.browser.page_source
                self.browser.execute_script("window.stop();")

            instance = BeautifulSoup(html, 'html.parser')
            html_parrent_info = instance.find('div', {'class': 'rvm-product-info'})
            item_view = html_parrent_info.find('div', {'class': 'view-count'})
            item_sold = html_parrent_info.find('div', {'class': 'item-sold-count'})

            html_sumary = instance.find('div', {'class': 'product-summary__content'})

            summary_raw_text = str(html_sumary)
            summary_removed_br = summary_raw_text.replace('<br/>', '[ENDLINE]')
            temp_instance = BeautifulSoup(summary_removed_br, 'html.parser')
            removed_multispace = re.sub('\ +', ' ', temp_instance.text.strip())
            removed_endline = removed_multispace.replace('\n', '')
            generate_new_endline = removed_endline.replace('[ENDLINE]', '\n')
            removed_outlier_space = generate_new_endline.replace('\n ', '\n')
            item_summary = removed_outlier_space

            good.dilihat = item_view.text
            good.terjual = item_sold.text
            good.informasi_produk = item_summary
            good.last_update = timezone.now()
            good.save()
            i += 1
