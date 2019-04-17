import requests
import json
from django.utils import timezone
from datetime import timedelta
from tokopedia.models import Shop, Good, GoodImage
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

cookies = ''
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def get_shop_page(link, full_return = False):
    try:
        shop_request = requests.get(link, headers = headers, timeout = 20)
        if full_return:
            return shop_request
        else:
            return shop_request.text
    except Exception as e:
        print('get_shop_page', str(e))
    return None


def get_shop_id(bs4):
    script = bs4.find_all('script')
    for i in script:
        if 'shop_id = ' in i.text:
            shop_id = i.text.split(' = ')[1].replace(';', '')
            return int(shop_id)
    return None


def get_shop_reputation(shop_id, full_return = False):
    api_link_old = 'https://www.tokopedia.com/reputationapp/reputation/api/v1/shop/350346?_=1543456451918'
    api_link = 'https://www.tokopedia.com/reputationapp/reputation/api/v1/shop/{}'

    try:
        shop_reputation_request = requests.get(api_link.format(shop_id), headers = headers, timeout = 20)
    except Exception as e:
        print('get_shop_reputation', str(e))

    assert shop_reputation_request.status_code == 200
    data = json.loads(shop_reputation_request.text)

    output = {
        'shop_score': int(data['data']['shop_score'].replace('.', '')),
        'shop_score_map': int(data['data']['shop_score_map']),
        'reputation_badge': data['data']['reputation_badge'],
        'reputation_badge_hd': data['data']['reputation_badge_hd'],
    }

    if full_return:
        return shop_reputation_request, output
    return output

def get_shop_etalase(shop_id, full_return = False):
    api_link_old = 'https://tome.tokopedia.com/v2/shop/350346/showcase'
    api_link = 'https://tome.tokopedia.com/v2/shop/{}/showcase'

    try:
        shop_etalase_request = requests.get(api_link.format(shop_id), headers = headers, timeout = 20)
    except Exception as e:
        print('get_shop_etalase:', str(e))

    assert shop_etalase_request.status_code == 200
    data = json.loads(shop_etalase_request.text)
    output = data['data']['showcase']
    for etalase in data['data']['showcase_group']:
        output.append(etalase)

    if full_return:
        return shop_etalase_request, output
    return output

def get_shop_note(shop_id, full_return = False):
    api_link_old = 'https://tome.tokopedia.com/v1/shop/shop_note?shop_id=350346'
    api_link = 'https://tome.tokopedia.com/v1/shop/shop_note?shop_id={}'

    try:
        shop_note_request = requests.get(api_link.format(shop_id), headers = headers, timeout = 20)
    except Exception as e:
        print('get_shop_note:', str(e))

    assert shop_note_request.status_code == 200
    data = json.loads(shop_note_request.text)
    output = data['data']['notes']

    if full_return:
        return shop_note_request, output
    return output

def get_shop_speed(shop_id, month_before = 1, full_return = False):
    api_link_old = 'https://slicer.tokopedia.com/shop-speed/cube/shop_speed_daily/aggregate?cut=shop_id:350346|finish_date:20181030-'
    api_link = 'https://slicer.tokopedia.com/shop-speed/cube/shop_speed_daily/aggregate?cut=shop_id:{}|finish_date:{}-'

    try:
        finish_date = (timezone.now() - relativedelta(months = month_before)).date()
        shop_speed_request = requests.get(api_link.format(shop_id, str(finish_date).replace('-', '')),
                                          headers = headers, timeout = 20)
    except Exception as e:
        print('get_shop_note:', str(e))

    assert shop_speed_request.status_code == 200
    data = json.loads(shop_speed_request.text)

    output = data['summary']

    if full_return:
        return shop_speed_request, output
    return output


def get_shop_products(shop_id, header = False, full_return = False):
    api_link_full = 'https://ace.tokopedia.com/search/product/v3?shop_id=350346&rows=1000&start=0&device=desktop&source=shop_product'
    api_link = 'https://ace.tokopedia.com/search/product/v3'
    params = {
        'shop_id': shop_id,
        'start': 0,
        'rows': 0,
        'device': 'desktop',
        'source': 'shop_product'
    }

    try:
        shop_product_request = requests.get(api_link, headers = headers,
                                          params = params, timeout = 20)
    except Exception as e:
        print('get_shop_note:', str(e))

    assert shop_product_request.status_code == 200
    data = json.loads(shop_product_request.text)

    total_data = data['header']['total_data']
    output = data['data']['products']

    if not header:

        main_list = []
        while len(main_list) < total_data:
            params['start'] = params['rows']
            params['rows'] += 200

            try:
                shop_product_request = requests.get(api_link,headers = headers,
                                                  params = params, timeout = 20)
            except Exception as e:
                print('get_shop_note:', str(e))

            assert shop_product_request.status_code == 200
            data = json.loads(shop_product_request.text)

            main_list += data['data']['products']
            print('\tObtaining ' + str(len(main_list)) + ' of ' + str(total_data))

        output = main_list

        # get full products
        # params['rows'] = total_data
        # try:
        #     shop_product_request = requests.get(api_link,headers = headers,
        #                                       params = params, timeout = 20)
        # except Exception as e:
        #     print('get_shop_note:', str(e))
        #
        # assert shop_product_request.status_code == 200
        # data = json.loads(shop_product_request.text)
        #
        # total_data = data['header']['total_data']
        # output = data['data']['products']

    if full_return:
        return shop_product_request, output, total_data
    return output, total_data

def get_good_view(product_id, full_return = False):
    api_link_old = 'https://tome.tokopedia.com/v2/provi?pid=359200081'
    api_link = 'https://tome.tokopedia.com/v2/provi?pid={}'

    try:
        shop_view_request = requests.get(api_link.format(product_id), headers = headers, timeout = 20)
    except Exception as e:
        print('get_shop_note:', str(e))

    assert shop_view_request.status_code == 200
    data = json.loads(shop_view_request.text)

    output = data['data']['view']

    if full_return:
        return shop_view_request, output
    return output

# sold, success, reject
def get_good_stats(product_id, full_return =False):
    api_link_old = 'https://js.tokopedia.com/productstats/check?pid=359200081'
    api_link = 'https://js.tokopedia.com/productstats/check?pid={}'

    try:
        goods_stats_request = requests.get(api_link.format(product_id), headers = headers, timeout = 20)
    except Exception as e:
        print('get_shop_note:', str(e))

    assert goods_stats_request.status_code == 200
    data = json.loads(goods_stats_request.text.replace('show_product_stats(', '').replace(')', ''))

    output = data

    if full_return:
        return goods_stats_request, output
    return output

# todo mengambil dan mengolah variasi goods
def get_good_variant():
    # childnya siapa aja, dsb
    api_link_old = 'https://tome.tokopedia.com/v2/product/359200106/variant'
    pass

def get_good_page(good_url, full_return = False):
    try:
        good_page_request = requests.get(good_url, headers = headers, timeout = 20)
        assert good_page_request.status_code == 200
        if full_return:
            return good_page_request, good_page_request.text
        return good_page_request.text
    except Exception as e:
        print('get_good_page:', str(e))
    return None


# todo: get rating -> sepertinya sudah ada
def get_good_rating():
    api_link_old = 'https://www.tokopedia.com/reputationapp/review/api/v1/rating?product_id=117316461'
    # rating_float = float(data['data']['rating_score'])
