from incap_cracker_py3.incap_session import IncapSession
import random

user_agent_list = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

def phase_one():
    session = IncapSession()
    session.headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': random.choice(user_agent_list),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'sec-gpc': '1',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'accept-encoding': 'gzip, deflate, br' 'accept-language: en-US,en;q=0.9'
    }
    phase_one_respone = session.get('https://www.vons.com')
    return session, phase_one_respone

session, phase_one_respone = phase_one()

adobe_headers = {
'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
'sec-ch-ua-mobile': '?0',
'user-agent': random.choice(user_agent_list),
'sec-ch-ua-platform': ('"Windows"'),
'accept': '*/*',
'sec-gpc': '1',
'sec-fetch-site': 'cross-site',
'sec-fetch-mode': 'no-cors',
'sec-fetch-dest': 'script',
'referer': 'https://www.vons.com/',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'Content-Encoding': 'gzip, delate, br'
}

response = session.get('https://assets.adobedtm.com/launch-ENd8a7ca47a5e943c9915bbea04a4d1b05.min.js', headers=adobe_headers)

get_adobe = session.get('https://dpm.demdex.net/id?d_visid_ver=5.5.0&d_fieldgroup=MC&d_rtbd=json&d_ver=2&d_orgid=A7BF3BC75245ADF20A490D4D%40AdobeOrg&d_nsid=0&d_coppa=true&ts=1701842003456', headers=adobe_headers)
adobe_payload = get_adobe.json()

{
    "d_blob": "6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y",
    "d_mid": "42428897325607849111554238748133982456",
    "d_ottl": 7200,
    "dcs_region": 9,
    "id_sync_ttl": 604800,
    "tid": "B1IC3244SFs="
}


session.cookies.set('AMCV_A7BF3BC75245ADF20A490D4D%40AdobeOrg', '179643557%7CMCIDTS%7C19698%7CvVersion%7C5.5.0')
session.cookies.set('AMCVS_A7BF3BC75245ADF20A490D4D%40AdobeOrg', '1')
session.cookies.set('mbox', 'session#43823667fa0448618e2a4edc6523a7fe#170184386')

response = session.get('https://www.vons.com/etc.clientlibs/wcax-core/clientlibs/clientlib-unified-site/vons.min.848ea48c4d3f677ee58c78766ce185c9.js', headers=adobe_headers)

response = session.get('https://www.vons.com/_Incapsula_Resource?SWJIYLWA=719d34d31c8e3a6e6fffd425f7e032f3&ns=1&cb=400937624', headers=adobe_headers)


okta_headers = {
'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
'sec-ch-ua-mobile': '?0',
'user-agent': random.choice(user_agent_list),
'sec-ch-ua-platform': ('"Windows"'),
'accept': '*/*',
'sec-gpc': '1',
'sec-fetch-site': 'cross-site',
'sec-fetch-mode': 'cors',
'sec-fetch-dest': 'empty',
'referer': 'https://www.vons.com/',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9'
}



okta_init = session.post('https://albertsons.okta.com/api/v1/sessions/me/lifecycle/refresh', headers=okta_headers)

next_header = {
'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
'sec-ch-ua-mobile': '?0',
'user-agent': random.choice(user_agent_list),
'sec-ch-ua-platform': ('"Windows"'),
'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
'sec-gpc': '1',
'sec-fetch-site': 'same-origin',
'sec-fetch-mode': 'no-cors',
'sec-fetch-dest': 'image',
'referer': 'https://www.vons.com/',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9'
}

next = session.get('https://www.vons.com/_Incapsula_Resource?SWKMTFSR=1&e=0.7572880114187579', headers=next_header)

next_header = {
'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
'sec-ch-ua-mobile': '?0',
'user-agent': random.choice(user_agent_list),
'sec-ch-ua-platform': ('"Windows"'),
'accept': '*/*',
'sec-gpc': '1',
'sec-fetch-site': 'same-origin',
'sec-fetch-mode': 'cors',
'sec-fetch-dest': 'empty',
'referer': 'https://www.vons.com/',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9'
}

next = session.get('https://www.vons.com/bin/safeway/unified/userinfo?rand=101454&banner=vons', headers=next_header)

test_header = {
'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
'sec-ch-ua-mobile': '?0',
'user-agent': random.choice(user_agent_list),
'sec-ch-ua-platform': ('"Windows"'),
'accept': 'application/json, text/javascript, */*; q=0.01',
'ocp-apim-subscription-key': '7bad9afbb87043b28519c4443106db06',
'x-requested-with': 'XMLHttpRequest',
'sec-gpc': '1',
'sec-fetch-site': 'same-origin',
'sec-fetch-mode': 'cors',
'sec-fetch-dest': 'empty',
'referer': 'https://www.vons.com/',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9'
}

test = session.get('https://www.vons.com/abs/pub/xapi/storeresolver/storeaddress?storeid=2053', headers=test_header)

next_header = {
'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
'sec-ch-ua-mobile': '?0',
'user-agent': random.choice(user_agent_list),
'sec-ch-ua-platform': ('"Windows"'),
'accept': 'application/json; charset=utf-8',
    'content-type': 'text/plain; charset=utf-8',
'sec-gpc': '1',
'sec-fetch-site': 'same-origin',
'sec-fetch-mode': 'cors',
'sec-fetch-dest': 'empty',
'referer': 'https://www.vons.com/',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9'
}

next = session.get('https://www.vons.com/ueene-suffe-and-swort-it-know-tenda-Enter-I-dist?d=www.vons.com', headers=next_header)

okta_header = {
'content-length': '82',
'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
'sec-ch-ua-mobile': '?0',
'user-agent': random.choice(user_agent_list),
'ocp-apim-subscription-key': '9e38e3f1d32a4279a49a264e0831ea46',
'sec-ch-ua-platform': ('"Windows"'),
'accept': 'application/vnd.safeway.v1+json',
'content-type': 'application/vnd.safeway.v1+json',
'x-swy-correlation-id': '0512e5f1-de18-4c24-bb33-24d796669092',
'x-swy-date': 'Wed, 06 Dec 2023 05:53:43 GMT',
'x-swy-client-id': 'web-portal',
'x-swy-banner': 'vons',
'sec-gpc': '1',
'sec-fetch-site': 'same-origin',
'sec-fetch-mode': 'cors',
'sec-fetch-dest': 'empty',
'referer': 'https://www.vons.com/',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9'
}

okta = session.get('https://www.vons.com/abs/pub/cnc/csmsservice/api/csms/authn/factors/password/okta/00ujkf8simeMNLmVH2p6/verify', headers=okta_header)