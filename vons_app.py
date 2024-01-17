from time import sleep
from get_session_cookies import run_logon, set_random_user_agent, final_refresh
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from incap_cracker_py3.incap_session import IncapSession


load_dotenv()


user_agent = os.getenv('user_agent')
username = os.getenv('username')
password = os.getenv('password')
store_id = os.getenv('store_id')
coupons = os.getenv('coupons')


cookie_file = '.cookies'


def set_user_agent():
    global user_agent
    user_agent = set_random_user_agent()
    return user_agent



def get_coupons(session, store_id, coupons):
    # You have a lovely website.  Now would you mind just giving me all my coupons?  Thanks.
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
    try:
        response = session.post(url=url, json=payload, timeout=5)
    except:
        print("Timeout clipping coupon")
    return response, session

def clip_all_coupons():
    session = generate_session()
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
    store_cookies(session, user_agent)





def generate_session():
    session_expired = True
    previous_cookies = get_previous_cookies()
    if not previous_cookies:
        set_user_agent()
        return run_logon(username, password)[0]
    cookies = previous_cookies.get('cookies')
    user_agent = previous_cookies.get('user_agent')
    for cookie in cookies:
        if cookie[0][:12] == 'visid_incap_':
            if datetime.fromtimestamp(cookie[4]) > datetime.now():
                session_expired = False
    if session_expired:
        return run_logon(username, password)[0]
    return rebuild_previous_session(cookies, user_agent)


def store_cookies(session, user_agent):
    all_cookies = []
    for cookie in session.cookies:
        all_cookies.append([cookie.name, cookie.value, cookie.domain, cookie.path, cookie.expires])
    cookies = {'cookies': all_cookies, 'user_agent': user_agent}
    with open(cookie_file, 'w') as f:
        f.write(json.dumps(cookies))


def get_previous_cookies():
    previous_cookies = None
    if os.path.exists(cookie_file):
        with open(cookie_file, 'r') as f:
            previous_cookies = json.loads(f.read())
    return previous_cookies



def rebuild_previous_session(cookies, user_agent):
    session = IncapSession()
    session.headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'sec-gpc': '1',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'sec-ch-ua': user_agent,
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'accept-encoding': 'gzip, deflate, br' 'accept-language: en-US,en;q=0.9'
    }
    for cookie in cookies:
        session.cookies.set(name=cookie[0], value=cookie[1], domain=cookie[2], path=cookie[3], expires=cookie[4])
    session, final_refresh_respons = final_refresh(session)
    if final_refresh_respons.status_code != 200:
        return run_logon(username, password)[0]
    return session




clip_all_coupons()