from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from tokopedia.models import Shop, Good, GoodImage, Etalase, Note, Category, Department
from bs4 import BeautifulSoup
import requests
import re
import tokopedia.api as toped_api

shop_link = [
    'https://www.tokopedia.com/armiashop'
]


class Command(BaseCommand):
    help = 'Clone Shop using requests'

    def __init__(self, stdout = None, stderr = None, no_color = False):
        self.options = None
        super().__init__(stdout, stderr, no_color)

    def add_arguments(self, parser):
        parser.add_argument('--link',
                            help = 'shop link')

    def handle(self, *args, **options):
        self.options = options

        if options['link']:
            print('Cloning', options['link'])

            html_shop_page = toped_api.get_shop_page(options['link'])
            bs4 = BeautifulSoup(html_shop_page, 'html.parser')

            shop = self.scrapShop(bs4)
            self.addGoods(shop, limit = 10)
            self.scrapGoodsDetail(shop)

    def scrapShop(self, bs4Instance):
        shop_id = toped_api.get_shop_id(bs4Instance)

        shop_header = bs4Instance.find('div', {'class': 'shop-header'})

        html_shop_link = shop_header.find('a', {'class': 'pull-left'})
        html_shop_name = shop_header.find('h1')
        html_shop_slogan = shop_header.find('div', {'class': 'slogan'})
        html_shop_quote = shop_header.find('div', {'class': 'shop-slogan'})

        key_images = shop_header.find_all('img', {'alt': html_shop_name.text.strip()})
        html_shop_cover_image_link = key_images[0]['src']
        html_shop_profile_image_link = key_images[1]['src']

        html_shop_terjual = shop_header.find('strong', {'id': 'shop-item-sold-v2'})
        html_shop_follower = shop_header.find('b', {'id': 'favorit-shop'})

        # print(html_shop_link['href'].strip())
        # print(html_shop_name.text.strip())
        # print(html_shop_slogan.text.strip())
        # print(html_shop_quote.text.strip())
        # print(html_shop_cover_image_link)
        # print(html_shop_profile_image_link)
        # print(html_shop_terjual.text.strip())
        # print(html_shop_follower.text.strip())
        # print(html_shop_speed['data-original-title'])
        # print(html_shop_reputation['data-original-title'])

        # get reputation
        shop_reputation = toped_api.get_shop_reputation(shop_id = shop_id)
        # get speed
        shop_speed_1 = toped_api.get_shop_speed(shop_id, month_before = 1)
        shop_speed_3 = toped_api.get_shop_speed(shop_id, month_before = 3)
        shop_speed_12 = toped_api.get_shop_speed(shop_id, month_before = 12)

        products, total_barang = toped_api.get_shop_products(shop_id, header = True)

        shop, created = Shop.objects.update_or_create(
            id = shop_id,
            toko_url = html_shop_link['href'].strip(),
            defaults = {
                'toko_id': shop_id,
                'toko_nama': html_shop_name.text.strip(),
                'toko_slogan': html_shop_slogan.text.strip(),
                'toko_quote': html_shop_quote.text.strip(),
                'toko_gambar': html_shop_profile_image_link,
                'toko_cover': html_shop_cover_image_link,

                'toko_terjual': html_shop_terjual.text.strip(),
                'toko_follower': html_shop_follower.text.strip(),

                'toko_1_bulan_speed': shop_speed_1['sum_speed'],
                'toko_1_bulan_order_count': shop_speed_1['order_count'],
                'toko_3_bulan_speed': shop_speed_3['sum_speed'],
                'toko_3_bulan_order_count': shop_speed_3['order_count'],
                'toko_12_bulan_speed': shop_speed_12['sum_speed'],
                'toko_12_bulan_order_count': shop_speed_12['order_count'],

                'toko_reputasi_score': shop_reputation['shop_score'],
                'toko_reputasi_level': shop_reputation['shop_score_map'],
                'toko_reputasi_badge_url': shop_reputation['reputation_badge'],

                'toko_jumlah_barang': total_barang,

                'last_update': timezone.now(),
            }
        )

        shop_etalase = toped_api.get_shop_etalase(shop_id = shop_id)
        for etalase in shop_etalase:
            if etalase['id'] == 0:
                Etalase.objects.update_or_create(
                    toko_induk = shop,
                    etalase_alias = etalase['alias'],
                    defaults = {
                        'etalase_id': etalase['id'],
                        'etalase_nama': etalase['name'],
                        'etalase_url': etalase['uri'],
                        'etalase_jumlah_produk': etalase['product_count'],
                    }
                )
            else:
                Etalase.objects.update_or_create(
                    id = etalase['id'],
                    toko_induk = shop,
                    etalase_alias = etalase['alias'],
                    defaults = {
                        'etalase_id': etalase['id'],
                        'etalase_nama': etalase['name'],
                        'etalase_url': etalase['uri'],
                        'etalase_jumlah_produk': etalase['product_count'],
                    }
                )

        shop_note = toped_api.get_shop_note(shop_id = shop_id)
        for note in shop_note:
            Note.objects.update_or_create(
                toko_induk = shop,
                id = note['shop_note_id'],
                defaults = {
                    'catatan_id': note['shop_note_id'],
                    'catatan_judul': note['title'],
                    'catatan_posisi': note['position'],
                    'catatan_uri': note['url'],
                    'catatan_last_update': note['last_update'],
                }
            )

        return shop

    def addGoods(self, shop, limit = None):
        shop_products, total_data = toped_api.get_shop_products(shop.toko_id)

        shop_data = shop_products[0]['shop']
        shop.toko_nama = shop_data['name']
        shop.toko_lokasi = shop_data['location']
        shop.toko_kota = shop_data['city']
        shop.toko_is_official = shop_data['is_official']
        shop.save()

        if limit:
            shop_products = shop_products[:limit]


        # reputasi tidak usah dicari karena barusaja

        for product in shop_products:
            # buat category dan department
            category, created = Category.objects.update_or_create(
                id = product['category_id'],
                defaults = {
                    'category_id': product['category_id'],
                    'category_name': product['category_name'],
                }
            )
            department, created = Department.objects.update_or_create(
                id = product['department_id'],
                defaults = {
                    'department_id': product['department_id'],
                    'department_name': product['department_name'],
                }
            )

            # sudah di scrap good detail
            # good_view = toped_api.get_good_view(product['id'])
            # good_status = toped_api.get_good_stats(product['id'])

            good, created = Good.objects.update_or_create(
                id = product['id'],
                toko_induk = shop,
                defaults = {
                    'barang_id': product['id'],
                    'barang_nama': product['name'],
                    'barang_url': product['url'].split('?')[0].strip(),
                    'barang_url_full': product['url'],
                    'barang_child': ', '.join([str(child_id) for child_id in product['childs']]) if product['childs'] else None,
                    'barang_parent_id': product['parent_id'],

                    'barang_gambar_utama': product['image_url'],
                    'barang_jumlah_kurir': product['courier_count'],
                    'barang_kondisi': product['condition'],

                    'barang_is_unggulan': product['is_featured'],

                    'barang_harga_asli': product['price_int'],

                    'barang_diskon_harga_asli': product['original_price'] if product['original_price'] else 0,
                    'barang_diskon_start': product['discount_start'],
                    'barang_diskon_expired': product['discount_expired'],
                    'barang_diskon_percentage': product['discount_percentage'],

                    'barang_stok': product['stock'],
                    'barang_status': product['status'],
                    'barang_is_preorder': product['is_preorder'],
                    'barang_minimal_order': product['min_order'],

                    # diletakkan di fungsi goods detail aja agar cepat
                    # 'barang_dilihat': good_view,
                    # 'barang_terjual': good_status['item_sold'],
                    # 'barang_transaksi_sukses': good_status['success'],
                    # 'barang_transaksi_gagal': good_status['reject'],

                    'barang_rating': product['rating'],
                    'barang_rating_count': product['count_review'],

                    'barang_category': category,
                    'barang_department': department

                }
            )

            # todo: get child ? -> call variant -> make the product
            # get child/variant? foreach -> make new product
            # for child in product['child']

            print('\tScrapping produk:', product['name'],
                  '[EDITED]' if not created else '')

    def scrapGoodsDetail(self, shop = None):
        if shop:
            unfinished_goods = Good.objects.filter(
                toko_induk = shop,
                barang_dilihat = None
            )
            if len(unfinished_goods) == 0:
                unfinished_goods = Good.objects.filter(toko_induk = shop,)
        else:
            unfinished_goods = Good.objects.filter(barang_dilihat = None)
            if len(unfinished_goods) == 0:
                unfinished_goods = Good.objects.all()

        for good in unfinished_goods:
            print('\tScrapping detail of', good.barang_nama)
            html_shop_page = toped_api.get_good_page(good.barang_url)

            instance = BeautifulSoup(html_shop_page, 'html.parser')

            # html_parrent_info = instance.find('div', {'class': 'rvm-product-info'})
            # item_view = html_parrent_info.find('div', {'class': 'view-count'})
            # item_sold = html_parrent_info.find('div', {'class': 'item-sold-count'})

            html_summary = instance.find('div', {'class': 'product-summary__content'})

            summary_raw_text = str(html_summary)
            summary_removed_br = summary_raw_text.replace('<br/>', '[ENDLINE]')
            temp_instance = BeautifulSoup(summary_removed_br, 'html.parser')
            removed_multispace = re.sub('\ +', ' ', temp_instance.text.strip())
            removed_endline = removed_multispace.replace('\n', '')
            generate_new_endline = removed_endline.replace('[ENDLINE]', '\n')
            removed_outlier_space = generate_new_endline.replace('\n ', '\n')
            item_summary = removed_outlier_space
            # print(item_summary)

            html_images = instance.find_all('div', {'class': 'content-img-relative'})
            for image in html_images:
                GoodImage.objects.update_or_create(
                    barang_induk = good,
                    gambar_url = image.img['src'],
                )

            good_view = toped_api.get_good_view(good.id)
            good_status = toped_api.get_good_stats(good.id)

            good.barang_dilihat = good_view
            good.barang_terjual = good_status['item_sold']
            good.barang_transaksi_sukses = good_status['success']
            good.barang_transaksi_gagal = good_status['reject']
            good.barang_informasi_produk = item_summary

            good.save()
