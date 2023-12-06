# The purpose of this script is to initiate traffic to vons.com.  Vons uses a tool called Incapsula to detect
# if the requester is human.  If not, it triggers a captcha challenge, which needs to be avoided.
# Rather than using a session object, this script reproduces the steps needed to retrieve the cookies
# that are used in subsequent requests to bypass incapsula.

# To determine the flow, I proxied my web traffic through mitmproxy, and analyzed the calls.  The below script
# is a combination of the functions I wrote, as well as some from https://github.com/ziplokk1/incapsula-cracker-py3
# which had already resolved some of my pain points.  Incapsula is set up site specific.  So this code likely
# wouldnt work on other pages.  But it can used as a model.  The key is the headers that are sent to the site.
# The site expects certain ones, which are unique to the page.  Also paramount is that the user agent header
# doesnt snitch you out.  This proved to be difficult to circumvent with the standard requests, and seleneum
# libraries.

import random
import subprocess
import httpx


### Utility Functions

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


# Known good user agent headers.  More should be added to prevent being blacklisted in the future.
user_agent_list = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

def initial_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Ch-Ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-Gpc': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

def get_incapsula_resource_url(phase_one_session, url):
    # Try to find specific url in session text
    found = False
    for item in phase_one_session.text.split():
        if '_Incapsula_Resource' in item:
            resource_url = item[6:-1]
            print('Found resource url')
            found = True
    if not found:
        print('Resource URL not found.  Generating random url.')
        rdm = random.random()
        resource_url = url + f'/_Incapsula_Resource?CWUDNSAI=1&e={rdm}'
    return resource_url

def get_incapsula_script_loc(phase_one_session, url):
    # Was getting this before, but seems to be iced out now. Statically setting url
    url = url + '/ueene-suffe-and-swort-it-know-tenda-Enter-I-dist'
    return url


def phase_one(domain='vons.com'):
    # if you do not have https, and/or www, vons.com will redirect you to https://www.vons.com.
    url = f'https://{domain}'
    user_agent = random.choice(user_agent_list)
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
    phase_one_session = httpx.get(url=url, headers=headers)
    if phase_one_session.status_code == 301:
        url = phase_one_session.headers.get('location')
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
        print(f'Initial call provided a 301 redirect to {url}')
        phase_one_session = httpx.get(url=url, headers=headers)
    if phase_one_session.status_code != 200:
        print('Blocked by Incapsula.  Ending script.')
        return
    cookie_visid_incap = ['visid_incap_1610354', phase_one_session.cookies.get('visid_incap_1610354')]
    cookie_nlbi = ['nlbi_1610354', phase_one_session.cookies.get('nlbi_1610354')]
    cookie_incap_ses = find_incap_ses_cookie(phase_one_session.cookies)
    incap_resource = get_incapsula_resource_url(phase_one_session, url)
    incap_url = get_incapsula_script_loc(phase_one_session, url)
    return url, cookie_visid_incap, cookie_nlbi, cookie_incap_ses, incap_resource, incap_url, phase_one_session


def phase_two(incap_url, cookie_visid_incap, cookie_nlbi, cookie_incap_ses):
    # Get the incap script
    visid_cookie = f'{cookie_visid_incap[0]}={cookie_visid_incap[1]}'
    nlbi_cookie = f'{cookie_nlbi[0]}={cookie_nlbi[1]}'
    incap_ses_cookie = f'{cookie_incap_ses[0]}={cookie_incap_ses[1]}'
    cookie_text = f'{visid_cookie}; {nlbi_cookie}; {incap_ses_cookie}'
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
    phase_two_session = httpx.get(url=incap_url, headers=headers)
    return phase_two_session



def isolate_incap_jscript(phase_two_session):
    full_js = phase_two_session.text

url, cookie_visid_incap, cookie_nlbi, cookie_incap_ses, incap_resource, incap_url, phase_one_session = phase_one()
phase_two_session = phase_two(incap_url, cookie_visid_incap, cookie_nlbi, cookie_incap_ses)
incap_js = phase_two_session.text
