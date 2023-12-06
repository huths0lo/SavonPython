from incap_cracker_py3.incap_session import IncapSession
import random

user_agent_list = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]


def find_incap_ses_cookie(cookies):
    incap_full, incap_key, incap_value = None, None, None
    cookie_strings = str(cookies).split()
    for item in cookie_strings:
        if item[:10] == 'incap_ses_':
            incap_full = item
            break
    i = 0
    if incap_full is not None:
        for character in incap_full:
            if character == '=':
                break
            i += 1
        incap_key = incap_full[:21]
        incap_value = incap_full[22:]
    return [incap_key, incap_value]


def get_incapsula_resource_url(phase_one_response, url='https://www.vons.com'):
    # Try to find specific url in session text
    found = False
    for item in phase_one_response.text.split():
        if '_Incapsula_Resource' in item:
            resource_url = item[6:-1]
            print('Found resource url')
            found = True
    if not found:
        print('Resource URL not found.  Generating random url.')
        rdm = random.random()
        resource_url = url + f'/_Incapsula_Resource?CWUDNSAI=1&e={rdm}'
    return resource_url


def phase_one():
    # Create session, and bypass incapsula.
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
    phase_one_response = session.get('https://www.vons.com')
    cookie_visid_incap = ['visid_incap_1610354', session.cookies.get('visid_incap_1610354')]
    cookie_nlbi = ['nlbi_1610354', session.cookies.get('nlbi_1610354')]
    cookie_incap_ses = find_incap_ses_cookie(session.cookies)
    return session, phase_one_response, cookie_visid_incap, cookie_nlbi, cookie_incap_ses








def phase_two(session):
    # initiate call to Okta
    url = 'https://albertsons.okta.com/api/v1/sessions/me/lifecycle/refresh'
    headers = {
        'content-length': '0',
        'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'accept': '*/*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'origin': 'https://www.vons.com',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.vons.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    phase_three_response = session.post(url=url, headers=headers)
    return session, phase_three_response


def phase_three(session, phase_one_response):
    # Finish Incapsula
    #session.cookies.set(name='___utmvc', value='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')
    resource_url=get_incapsula_resource_url(phase_one_response)
    session.headers = {
        'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'image',
        'referer': 'https://www.vons.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    phase_three_response = session.get(resource_url)
    return session, phase_three_response



def phase_four(session):
    # Get user cookie
    url = 'https://www.vons.com/bin/safeway/unified/userinfo?rand=101454&banner=vons'
    session.headers = {
        'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.vons.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    phase_four_response = session.get(url)
    return session, phase_four_response

def phase_five(session):
    # Complete Okta
    url = 'https://albertsons.okta.com/oauth2/ausp6soxrIyPrm8rS2p6/v1/authorize?client_id=0oap6ku01XJqIRdl42p6&redirect_uri=https://www.vons.com/bin/safeway/unified/sso/authorize&response_type=code&response_mode=query&state=joyous-boy-camden-obeisant&nonce=ovJgrUobDYQKhiownVT9jU1GvtkRdpC4Eoyal2SfgGu6ezXG5b03393l08xbDGw8&scope=openid%20profile%20email%20offline_access%20used_credentials&sessionToken=20111p7BWShOmlAIP3XQBvNTSz207eTAoPEozE9inKzjwNqKe_tJbnK'
    session.headers = {
        'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.vons.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    phase_five_response = session.get(url)
    return session, phase_five_response

def phase_six(session):
    # Complete Okta
    url = 'https://www.vons.com/bin/safeway/unified/sso/authorize?code=_Q16nrSgJiGznZFxndq_B5loXJ0hW2wysXrs8ho8u6o&state=joyous-boy-camden-obeisant'
    session.headers = {
        'upgrade-insecure-requests': '1',
        'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.vons.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    phase_six_response = session.get(url, True)
    return session, phase_six_response


{
    "d_blob": "6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y",
    "d_mid": "42428897325607849111554238748133982456",
    "d_ottl": 7200,
    "dcs_region": 9,
    "id_sync_ttl": 604800,
    "tid": "B1IC3244SFs="
}
phase_one_session, phase_one_response, cookie_visid_incap, cookie_nlbi, cookie_incap_ses = phase_one()
phase_two_session, phase_two_response = phase_two(phase_one_session)
phase_three_session, phase_three_response = phase_three(phase_two_session, phase_one_response)
phase_four_session, phase_four_response = phase_four(phase_three_session)
phase_five_session, phase_five_response = phase_five(phase_four_session)
phase_six_session, phase_six_response = phase_six(phase_five_session)


### Below are notes

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