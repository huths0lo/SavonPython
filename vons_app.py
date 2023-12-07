from time import sleep
from get_session_cookies import run_logon, set_random_user_agent
import os
from dotenv import load_dotenv


load_dotenv()


user_agent = os.getenv('user_agent')
username = os.getenv('username')
password = os.getenv('password')
store_id = os.getenv('store_id')
coupons = os.getenv('coupons')





def set_user_agent():
    global user_agent
    user_agent = set_random_user_agent()
    return user_agent



def get_coupons(session, store_id, coupons):
    url = f'https://www.vons.com/abs/pub/xapi/offers/companiongalleryoffer?storeId={store_id}&rand={coupons}'
    session.headers = {
        'user-agent': user_agent,
        'sec-ch-ua': user_agent,
        'accept-encoding': 'gzip, deflate, br',
        'connection': 'keep-alive',
        'x-swy_api_key': 'emjou',
        'x-swy_version': '1.1',
        'x-swy-Application-Type': 'web',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'accept-language': 'en-US,en;q=0.9'

    }
    all_coupons = session.get(url=url, timeout=30)
    if all_coupons.status_code == 200:
        all_coupons = all_coupons.json()
        all_coupons = all_coupons['companionGalleryOfferList']
    else:
        all_coupons = {}
    return all_coupons, session


def get_all_unclipped(all_coupons):
    unclipped = []
    for item in all_coupons[0]:
        if item['status'] == 'U':
            unclipped.append([item['offerId'], item['offerPgm'], item['name']])
    return unclipped


def post_clip(session, clip_id, item_type, store_id):
    url = f'https://www.vons.com/abs/pub/web/j4u/api/offers/clip?storeId={store_id}'
    session.headers = {
        'user-agent': user_agent,
        'sec-ch-ua': user_agent,
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'accept-language': 'en-US,en;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'connection': 'keep-alive'
    }
    payload = {"items":[{"clipType":"C","itemId":str(clip_id),"itemType":item_type},{"clipType":"L","itemId":str(clip_id),"itemType":item_type}]}
    response = session.post(url=url, json=payload, timeout=30)
    return response, session

def clip_all_coupons():
    global session
    set_user_agent()
    session, logon_response = run_logon(username, password)
    all_coupons = get_coupons(session, store_id, coupons)
    unclipped = get_all_unclipped(all_coupons)
    total_clipped = 0
    for coupon in unclipped:
        clip_id = coupon[0]
        item_type = coupon[1]
        item_name = coupon[2]
        response, session = post_clip(session, clip_id, item_type, store_id)
        total_clipped += 1
        print(f'Clipped coupon {clip_id} {item_name}.  Total clipped = {total_clipped}')
        sleep(.1)
    print('\n\nProcess Completed!')


clip_all_coupons()