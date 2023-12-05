import random
import httpx


user_agent_list = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]




def phase_one_two():
    incap_resource = None
    url = 'https://vons.com/'
    headers = {
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
    phase_one = httpx.get(url=url, headers=headers)
    url = 'https://www.vons.com/'
    headers = {
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
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0'
    }
    phase_two = httpx.get(url=url, headers=headers)
    visid_incap_1610354 = phase_two.cookies.get('visid_incap_1610354')
    nlbi_1610354 = phase_two.cookies.get('nlbi_1610354')
    incap_ses_1360_1610354 = phase_two.cookies.get('incap_ses_1360_1610354')
    for item in phase_two.text.split():
        if '_Incapsula_Resource' in item:
            incap_resource = item[6:-1]
    return visid_incap_1610354, nlbi_1610354, incap_ses_1360_1610354, incap_resource

def phase_three(incap_resource,incap_ses_1360_1610354, visid_incap_1610354):
    url = (f'https://www.vons.com/{incap_resource}')
    cookie_text = f'incap_ses_1360_1610354={incap_ses_1360_1610354}; visid_incap_1610354={visid_incap_1610354}'
    headers = {
        'user-agent': random.choice(user_agent_list),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'sec-gpc': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'cookie': cookie_text
    }
    response = httpx.get(url=url, headers=headers)
    return response

def run_auth():
    visid_incap_1610354, nlbi_1610354, incap_ses_1360_1610354, incap_resource = phase_one_two()
    response = phase_three(incap_resource,incap_ses_1360_1610354, visid_incap_1610354)
    return response