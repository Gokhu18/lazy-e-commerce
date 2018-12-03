from django.test import TestCase
from bs4 import BeautifulSoup
import tokopedia.api as toped_api
import json

cookies = ''
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# Create your tests here.
class APITest(TestCase):
    def test_get_shop_page(self):
        result = toped_api.get_shop_page('https://www.tokopedia.com/armiashop', full_return = True)
        self.assertIsNotNone(result)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(result.text.startswith('<!DOCTYPE html>'))
        self.assertTrue(result.text.endswith('</html>'))

    def test_get_shop_id(self):
        result = toped_api.get_shop_page('https://www.tokopedia.com/armiashop')
        instance = BeautifulSoup(result, 'html.parser')
        shop_id = toped_api.get_shop_id(instance)
        self.assertIsNotNone(shop_id)
        self.assertTrue(isinstance(shop_id, int))

    def test_get_shop_reputation(self):
        result, output = toped_api.get_shop_reputation(shop_id = 350346, full_return = True)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result.status_code, int))
        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(result.text)

        data = json.loads(result.text)
        self.assertEqual(data['status'], 'OK')
        self.assertTrue(isinstance(int(data['data']['shop_score'].replace('.', '')), int))
        self.assertTrue(isinstance(int(data['data']['shop_score_map']), int))
        self.assertTrue(isinstance(data['data']['reputation_badge'].replace('.', ''), str))
        self.assertTrue(isinstance(data['data']['reputation_badge_hd'].replace('.', ''), str))

        self.assertTrue(isinstance(output, dict))
        self.assertTrue(isinstance(output['shop_score'], int))
        self.assertTrue(isinstance(output['shop_score_map'], int))
        self.assertTrue(isinstance(output['reputation_badge'], str))
        self.assertTrue(isinstance(output['reputation_badge_hd'], str))

    def test_get_shop_etalase(self):
        result, output = toped_api.get_shop_etalase(shop_id = 350346, full_return = True)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result.status_code, int))
        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(result.text)

        data = json.loads(result.text)
        self.assertEqual(data['status'], 'OK')

        self.assertTrue(isinstance(output, list))
        for etalase in output:
            self.assertTrue(isinstance(etalase['id'], int))
            self.assertTrue(isinstance(etalase['name'], str))
            self.assertTrue(isinstance(etalase['alias'], str))
            self.assertTrue(isinstance(etalase['uri'], str))
            self.assertTrue(isinstance(etalase['product_count'], int))

    def test_get_shop_note(self):
        result, output = toped_api.get_shop_note(shop_id = 350346, full_return = True)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result.status_code, int))
        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(result.text)

        data = json.loads(result.text)
        self.assertEqual(data['status'], '1')
        self.assertTrue(isinstance(output, list))

        for note in output:
            self.assertTrue(isinstance(note['shop_note_id'], int))
            self.assertTrue(isinstance(note['title'], str))
            self.assertTrue(isinstance(note['position'], int))
            self.assertTrue(isinstance(note['url'], str))
            self.assertTrue(isinstance(note['last_update'], str))

    def test_get_shop_speed(self):
        for month in [1, 3, 12]:
            result, output = toped_api.get_shop_speed(shop_id = 350346, month_before = month, full_return = True)
            self.assertIsNotNone(result)
            self.assertTrue(isinstance(result.status_code, int))
            self.assertEqual(result.status_code, 200)
            self.assertIsNotNone(result.text)

            data = json.loads(result.text)
            self.assertTrue(isinstance(data['summary'], dict))
            self.assertTrue(isinstance(data['summary']['sum_speed'], int))
            self.assertTrue(isinstance(data['summary']['order_count'], int))

            self.assertTrue(isinstance(output, dict))
            self.assertTrue(isinstance(output['sum_speed'], int))
            self.assertTrue(isinstance(output['order_count'], int))

    def test_get_shop_products(self):
        result, products, total_data = toped_api.get_shop_products(shop_id = 350346, header = True, full_return = True)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result.status_code, int))
        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(result.text)

        data = json.loads(result.text)

        self.assertTrue(isinstance(products, list))
        self.assertTrue(isinstance(total_data, int))
        self.assertEqual(len(products), 0)


        result, products, total_data = toped_api.get_shop_products(shop_id = 350346, full_return = True)
        self.assertTrue(isinstance(products, list))
        self.assertTrue(isinstance(total_data, int))
        self.assertEqual(len(products), total_data)

        for product in products:
            self.assertTrue(isinstance(product['id'], int))
            self.assertTrue(isinstance(product['name'], str))
            self.assertTrue((isinstance(product['childs'], list) or product['childs'] is None))
            self.assertTrue(isinstance(product['parent_id'], int))
            self.assertTrue(isinstance(product['url'], str))
            self.assertTrue(isinstance(product['image_url'], str))
            self.assertTrue(isinstance(product['shop'], dict))
            self.assertTrue(isinstance(product['courier_count'], int))
            self.assertTrue(isinstance(product['condition'], int))

            self.assertTrue(isinstance(product['category_id'], int))
            self.assertTrue(isinstance(product['category_name'], str))
            self.assertTrue(isinstance(product['department_id'], int))
            self.assertTrue(isinstance(product['department_name'], str))
            self.assertTrue(isinstance(product['badges'], list))

            self.assertTrue(isinstance(product['is_featured'], int)) # produk unggulan
            self.assertTrue(isinstance(product['rating'], int))
            self.assertTrue(isinstance(product['count_review'], int)) # jumlah ulasan

            self.assertTrue(isinstance(product['price_int'], int)) # harga

            self.assertTrue(isinstance(product['original_price'], str))
            self.assertTrue(isinstance(product['discount_start'], str))
            self.assertTrue(isinstance(product['discount_expired'], str))
            self.assertTrue(isinstance(product['discount_percentage'], int))

            self.assertTrue(isinstance(product['stock'], int))
            self.assertTrue(isinstance(product['status'], int))
            self.assertTrue(isinstance(product['is_preorder'], bool))
            self.assertTrue(isinstance(product['min_order'], int))

    def test_get_good_page(self):
        good_page = 'https://www.tokopedia.com/laris88/payung-magic-3d-muncul-motif-jika-basah-bonus-sarung-payung'
        result, output = toped_api.get_good_page(good_page, full_return = True)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result.status_code, int))
        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(result.text)
        self.assertTrue(result.text.startswith('\n<!DOCTYPE html>'))
        self.assertTrue(result.text.endswith('</html>\n'))

    def test_get_good_view(self):
        result, output = toped_api.get_good_view(359200081, full_return = True)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result.status_code, int))
        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(result.text)

        self.assertTrue(isinstance(output, int))

    def test_get_good_stats(self):
        result, output = toped_api.get_good_stats(359200081, full_return = True)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result.status_code, int))
        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(result.text)

        self.assertTrue(isinstance(output, dict))
        self.assertTrue(isinstance(output['item_sold'], int))
        self.assertTrue(isinstance(output['success'], int))
        self.assertTrue(isinstance(output['reject'], int))



