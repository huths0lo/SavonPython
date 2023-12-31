from incap_cracker_py3.incap_session import IncapSession
import json
import random
import time
import re



user_agent = None





USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"'
    ]

def set_random_user_agent():
    global user_agent
    user_agent = random.choice(USER_AGENT_LIST)
    return user_agent

def find_incap_ses_cookie(cookies):
    incap_full, incap_key, incap_value = None, None, None
    cookie_strings = str(cookies).split()
    for item in cookie_strings:
        if item[:10] == 'incap_ses_':
            incap_full = item
            break
    #i = 0
    if incap_full is not None:
        for character in incap_full:
            if character == '=':
                break
            #i += 1
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
    phase_one_response = session.get('https://www.vons.com')
    cookie_visid_incap = ['visid_incap_1610354', session.cookies.get('visid_incap_1610354')]
    cookie_nlbi = ['nlbi_1610354', session.cookies.get('nlbi_1610354')]
    cookie_incap_ses = find_incap_ses_cookie(session.cookies)
    return session, phase_one_response, cookie_visid_incap, cookie_nlbi, cookie_incap_ses








def phase_two(session):
    # initiate call to Okta.  Get a placeholder cookie.  This also is always a 400 status code.
    # Basically okta doesnt know who you are, so it responds as not authorized, and gives you a token to come back with later.
    url = 'https://albertsons.okta.com/api/v1/sessions/me/lifecycle/refresh'
    headers = {
        'content-length': '0',
        'sec-ch-ua': user_agent,
        'accept': '*/*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
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
    phase_two_response = session.post(url=url, headers=headers)
    return session, phase_two_response


def phase_three(session, phase_one_response):
    # Finish Incapsula.  In a web browser, this would be called up in a hidden iframe, using the tokens recieved at this point.  The url is highly obfuscated within the js payload.  We're getting the info, and making that call here.
    # You get.... another cookie.
    resource_url=get_incapsula_resource_url(phase_one_response)
    url = 'https://www.vons.com/' + resource_url
    session.headers = {
        'sec-ch-ua': user_agent,
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'image',
        'referer': 'https://www.vons.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    phase_three_response = session.get(url, True)
    return session, phase_three_response



def phase_four(session):
    # Get user cookie...another damn cookie
    url = 'https://www.vons.com/bin/safeway/unified/userinfo?rand=101454&banner=vons'
    session.headers = {
        'sec-ch-ua': user_agent,
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
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
    # Complete Okta - Part 1
    okta_nonce, okta_key, script_Tegridy, state_token = None, None, None, None
    url = 'https://albertsons.okta.com/oauth2/ausp6soxrIyPrm8rS2p6/v1/authorize?client_id=0oap6ku01XJqIRdl42p6&redirect_uri=https://www.vons.com/bin/safeway/unified/sso/authorize&response_type=code&response_mode=query&state=joyous-boy-camden-obeisant&nonce=ovJgrUobDYQKhiownVT9jU1GvtkRdpC4Eoyal2SfgGu6ezXG5b03393l08xbDGw8&scope=openid%20profile%20email%20offline_access%20used_credentials&sessionToken=20111p7BWShOmlAIP3XQBvNTSz207eTAoPEozE9inKzjwNqKe_tJbnK'
    session.headers = {
        'sec-ch-ua': user_agent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
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
    okta_nonce_search = re.search(r"nonce=\"(.*?)\"", phase_five_response.text)
    okta_key_search = re.search(r"okta_key&#x3d;(.*?)\"", phase_five_response.text)
    script_Tegridy_search = re.search(r"mainScript.integrity = \'(.*?)'", phase_five_response.text)
    state_token_search = re.search(r"stateToken=(.*?)'", phase_five_response.text)
    if okta_nonce_search and okta_key_search and script_Tegridy_search and state_token_search:
        okta_nonce, okta_key, script_Tegridy, state_token = okta_nonce_search.group(1), okta_key_search.group(1), script_Tegridy_search.group(1), state_token_search.group(1)
    okta_date = phase_five_response.headers.get('Date')
    return session, phase_five_response, okta_nonce, okta_key, script_Tegridy, state_token, okta_date

def phase_six(session):
    # Complete Okta - Part 2
    url = 'https://www.vons.com/bin/safeway/unified/sso/authorize?code=_Q16nrSgJiGznZFxndq_B5loXJ0hW2wysXrs8ho8u6o&state=joyous-boy-camden-obeisant'
    session.headers = {
        'upgrade-insecure-requests': '1',
        'sec-ch-ua': user_agent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
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


def get_token(session):
    # This is the imperative token that identifies you as human, and the ultimate conclusion of the Incapsula process.
    # This token is delivered in the response, but not as in a set-cookie header.  We have to grab it and inject it in to our session.
    # "dnclip" for those of you as old as I am.
    payload = {"solution":{"interrogation":{"p":"/H0sALk7xvL1P4iNZoGQoWXWUr1KmUw+A5ZBsqbWP7cqSS2PST3CRk4tlEeuS+g79ZXIOatVEE2wBpb6k1nF5xuZq9dJlRqme6FeSU/RCoKz51Kod2keyR5krG5MMLx4jDLxF+icigz6NDAKxmKMtbgXkqI5z6XbWvk4iXPKFjEGkH2y9dBh01FyXZAwA988UBSGJ9x7pHSelqBGi3d9LuxZvrPNPajQP8PPpHqHWdIK2wQSNp1doYj7BaBGVUOwOkCyX04Zg3P6UI13vsXneOAMLE6zCcLP5i/g0SjZ24AB2FarcI04KjfPKsiIwCvdBDkY7Gtmh3lKDp9W3GaFJ8u8oQj3NHMDs0Csx9EKm7NznbeWHLlSsHeIX3xU5D7H36te9yYEO81ORIQFEmLlBdNolFOC9LEX9n1gB7Yi7PiNRdHzH5uv+Vq8fcU77S85MdUy4d/8Iq1QOiXTUTPICmMynF+lWPwowcLFdaJ7YTbafY38zSSprWSY9618uEurbohfXH/FEt/vh2zoKipU/y1Vj3NaK/sf8xTSEsfB00uvIDYf/2ac6cxmqaEy1ve8e6R7njvZMQcOlw/Rl/FFt0x0U5g9HNMMG17gRpMwzRvT/sVUql53CLgX783mLo6oOsPVrSDHB7RBgmhcb+Yx+sG6WdMoRWGILl+/U24RkHGsSY9bnImuDZRfVhTaUcHtmEH21zv9ledkoi+6RIxkX1vnA8nP6C22aEg4xBc4/zozeOInyXitDbipngeRQAp4uQ39kb1HyLFsvKDnbZJI+FCpXUsDsS7QxaBA9Qw0NM4fI/wfCmHQO89lmUbhmcok/Cp2TIwN7NzuHaunOfv5oyfdMJZTqX5xb9Q2r/DDeolwHmiaMwDQLzIVmV2GDf4a19b2c4t6ZxuuVKm8yzWwlE+tmLo94RGnBP1TXx+iQ7rwhVeiMl5tpQQ6xENMJfoNxXyEfomSohfbVh1ugBD81+EvqoB79siDG7NI7kexbEZQ6xzl8odQ1zIECaQ0EPIvGV/ySJsujCfKyvpErH02Q/J1nYGfaenEIuTVrx3eUNY28hkubNdJiJPnNqZAan+tGQSZRm0LlHyAIegR1sfXQIJcVwTXQoSVpk370BXxzLNioXHHA/gTKwjtKtLvv3WGYW0T0X5QondqN7oYjmyLSaKYjwvhbVcQ0yHn9MEtuLtGgpf2VIhE2Cn9Lz55m0SNzOg2r3MCdqg9DMI6JkWGIaoaxBz/7aUT5QQVfs1Yk6/CLJKPXJy0lymOApV1knFAe51WpZLuL7pfb2CNLgL6DBVR1BHqXKZNpKS2EM4EM2zDb7GloUycokvM0vEuiUP/PeVXQGuJRY/OrG/PXm17jwcY5CIdSslvvSTcJMLQ+0W6MTdS53K80NQZxdpBsbjMUZRg1i6KTE9x9DbazrlWp2ZKWfVUK8MwJHb4LtFOuma2gJZ2sEZ3I8QoqpHhKpeTT6mk3GWYSvdV8CUKI4BFh7fnAqo1AQDhQ2mBZkcSgniFY8ACyObwYLhZeS3YK62Hpg2ok0O5oft7q3DmRqNrQwvrK9TPijazWEF/vT8GxSE5e8JjjDPFBruWrwT+JGcYzniAlYYnqNNPy8a9Z90+1DTxJSMqyT/B2rkPgx0fN/VIcptaTg3dLt1mwwC0sLEYxTcOS+RAh46ePoiVCc7jkRTVA6NK61lJT/0o68uwROwmNka6Okaee3AgrFmFDa9J+f7KTtU/L1e4A9jXo1/8/DfB9qsJwS+SbLgFFCKHUpvdo0LoEBltgzNJrV0/Y9sblDLULdv+42aLW14BsxHh9/gLqYhWibr9Y8oUoUDkUFNb2DTM/oZYwQdkSJM5RY0AHkfCFu4TxSbTxvYTxAU/RI0mw9D4LbuHSorhqinqZvYr/0hsKs4K57uSQ9gSY220G3mXEWUfxmO+IPwd2enhebR+egn/aPjj9x2Agm2/l8pUolmyE8pgRQGeXo7JmkvLNQY16EF9jX51LLdgjSr9XLCRlTTqEyhVpz3dwP5T29A29sGwDa1F22C+eUwIj1Xdx+MWvVk6KsZ1e6AlN3znAPMUwh2gqI8p7AVHG7AG/8i9d+uTSZWc5VS9RfMSqx5paM8roJ3ENq1BXUyEVFy6a1IjqlqnItx/oJW1EM1dGkiaLPbfsk3o6wfewoAg5Q6+X6JMelPyDdXxhmHubA4n9khF3VkwZ+0p307rUrS+nxiEUngO/lChkKcQrY9PkriEXL1SygPVOA4tzwSQseM3zSETN50pUY0LBWP9Cv5Zplbm4qMY5z45QP1GirqkbvnbF5qZz1e3Y8RgpkhbeM8kyc+oet8dDwDxPi/jbmAlp1+tF8k0+9z4aqEjJl2uOPfaxmrAxjjlz4gL3l/uFeA3LwiaU53boBeORVwthFNQg1o0SMEF7VOQW7KauBPMJhpctQz/8u0kodpCk6/xKssZhS2IPjI0l3CjtsEvgUxgULA2GtxdfjWQOc1603KO4+sA308Nbt5Wh46gU8POCvPbnEyTR+UUvn0NDosd4t6LP5sZEAPxRTvcCShfzjf6GOch/oSCCMI/B1SGCcnK7UXZ3iLF2P5uzD24EOU4IwfiBt75g27vCANqkAQmxiAafsUA/X63E8fwsRbAHQF6hDCqsdgyvaxysdqLV6xl1SD1HXRh+R/8v95u5gZsG+9KYPsMB1j+KuNeqE7k56cgoGlTAMoi3+eWerGqTsr4hlajd9Iz6BsqHKZBrpy+ecgDPRbLfFKObUQlqwOMJMQu7+7STJJvTxSkKcrX2TTh5nr9yrcp/ySsbZh/bV79GfDtzyGtYwEC8SIy9m0Gce8N/0mPXJ2dp0CAaih2nCj3xsgklKpDrrPHAMsmrFf1CD0FsWqyius3mndHd45Yd7xeMlLxDoNmvV+smJBztF1tEsZI09zDb++SCtfriFKlbJVHoxMZDu1y++CDP7h9T2vKG2e3Nwhf0Tnmf90+kOTPSaRmIV2tRdzAzgKlgWivg6YD/RyKVIxbKzCsd66M7ibQI0tCqRds8CsydalThCztC8jC6X2nXXgjxCyup9Yczd0iz+G8HcAI6y7EDg5OpEPT8oxC4AoeFONhH9oUASGRWoZnkVego5ARxx9fDOF2pqXaMOGcVK6b62a/YPMxxjAbE/cB8bL0JpFeQ2yxJQbuPAhSiXSGf4pL+vXqbpRkVhfwHPr6iUXC4xzr5KQH7h60SrF1Ykr9M8Dy1RmIQENrqgwO1hAlVOgr0W2uTObs00PHLwhap1e916B11qx+vafSS6IjskzqAhlD2Ee3hvIFlEp1Q7xvaJVvHzj/XrYj4he9qIopwU5Wcpovyv34EbSFfYvooS7JMs8m9QQDEKQ7tbb9Dqp6YlD9Qz/EIiFCwziuSI0w/fjhSKApbEWvXbKLqXbw6THz4MpWqVylAaUXBEDeK6eiwiSQSVVd9mFFrFRBZ8o/9BLFeJijoCHbCipU6GW7lqhe1tIv3uC3bYtbzmyvHQlMyyDh2/88qmJaL+06Iss4ACCLXd1+3hjcsY9rjW91F9pOoLC0HZ3jBvDDqAzwPdoBoUpjdegJxfqjEKdsByn/TjDzIB1+9wLtRb8GrKSiJ/lpSx/eUrmtpH/L0Rzg07UfxBiTc6xRVnbkB/nTln7TAzFB7U5rjEtHMOAz6FuvccCptg3BQmkAq12huKgBpKRFw8uXTosF5y/+KBMmllXBwbhVoiQuIo07JsgrBHL+LKQn1DyLg91plh4PXY0i5czGB5XuBviIrAbuFp531wUvD5dah4fZP6prHmjIbWmCTF0JpX6WE8oO3aaRc41/fVuHdLuWoQvY2wfF37s/11q6Acp8CQK3W9TvzQC2SUNVhyUZ6StGB79WhGS+aL2QiQ/JAzxhp1asnJ9W2vsytIbSbZ524z7kMkhBoki3p51Q5T0dN8JfRJ5uW3n0D8VTgV6sjLcNxUpAAs1srJL7N72ie7WFwVCgVc49xicPDolo5OSFOZVGVFqzYHOzQSx58jHgU4RsmICbOe8sDmeTNuXS3xWSnVieq4Ej1UOnD8gGDEShYZS/5CaxQVNynAgRjlByUMofnyDXDcrn4numRwFXkgv06NcYipt2qrTKdr1e5hW3Vic/iV+i4MIPgn5NO/UpM/AQfB+9e+lJrgvc1NBam3dxS5ko95qTYdDaHfmJ1k2XbMothmFFAeM13NqobtQPFz7qY1OgXlAbkWKfIPxFooihCug+OF2gNuXW+xLG3Rn978lisD+Md7FGXUShRbiiij6kfUNMpAYF9xQqbOsy6WKZbJmumyXZGy4G01TWu6tY8tIx4/qicswkpWGqYnUvqG6f3rlu2wtjZrkuMtYSfQiNVqMUwAHs/9gguHNzKuUS1N7ZKL2MRKHPiw/cIbtJj15oT6Vdn6b5RLVVX1KuPCLeWVUskzrsTbJjn+X4UaopEmm5MtLc7CCIs3Snl9VQpy6Ee68THgy6dIC37ivHWjYp1HYNkFNBPeFClQajYKOxjD7CKi1FjXeZgalShYZNgJ7YeN4hyzOXRkEIsUu3nNsTkmpBKPR9BZ5SQiiMdb4a2wDN3N4m2QxMbZF9mZmzedzzb6638m6pQMA6zjFLXaF8sK/nMINOWnLdanamVj1gwDe4JIMg58nMb5oSU2m0FcT6yD+xs16eqo8s11r+GOkaNCirXa2XxBaPHgwf/25fnEpSA9534Qv3P/WcxlGuU2Q39XumzLpgxcIJhLfqQ6pjh1+gT3lZwSztrZNhiXZ5XqEMBuRpCmnjCMFemUiqso834ChpLedDge7GP4i4Y7Sq42q5MI8w0Rthao9MwuLCB6dDUnCvET7+Li1vtnHnXIFUpIC2Mul5XHzIM9XswS2s0Cv7+oxWqCCEW7lNdjfULPC67RO9bHViiQEJzTYuSfgP/mWxaKGAo0WlWmYY6maK+/cMoKNojLjOfN4D4jjSBy8WnVGjmbxxgkgiEOR4c59MdBGtU7gd2XiOgoIf1AQwRphjn7e/fenJMfCb2nzbCpo95xhvLrNblrKSf9cVGA/5dESiTHZU0gT2VIxxnIjWRKprYj3xQpObuETy1D/ox+N73wyuB9YdDSjUHIi/l0riEwUa1WVjnWhZDaJCkibfOvqMxW+VASEfojjz2qR01NQ8o578dq1ftQqoQWh9xAbZ4rdKuV1fcKl4HtUkRxvGeKca+Dj10MBbwCwlQ/5k9fvOM7zEIc+lmSnfCI51hU1nLrVKmo7ZMrAhMy2CMhPfCBtjvEaFGMYS5OO5C9caGjPCNdvLtVuOgES7mP1GmkbZLIZGdSuMRM/33wj7AxMn6EZZpVNBKqwF0nmffpen5GGvbi5RhBD1mrVY65pGv7PZS4JavmutTWEpzg/+5KdV1U5gEPpsEfYIYiKsX4hrkWmcqexOg1lvOc472OTxHr6ARYuxzRP4BoVSjXJbH4lKob7nOblAU16TOwrVNgJHm32QBdYwhfTDdq18RjHBSZb1wxqGjhLV9I5VoiuRSK5RYzmjXIGA1iecXVBDmgw/9nBTI6UHjCjbL+eU0UunXkMK5hbt0eACtJBDjrLPbtRfpnKMemxn8jz/zuwNvXJGK/1YXIZlDG3WDOAL7TyP4uRbn0heBecL+9XmMoGYV6S+mRvGSfkE9x4oas0V/+GhE7Z5RW7BED/QARhmtw3mQvkjw+beP6BhZj7Kb/bZzgfUxyn84rUKrX/YHMA8SU3SM9HvpFL1EAU3hA01qyoAXY1bqA3kPtTcnQyMDhlMhCmyn4lV2uIs6sX9UZZGp2TFd3IsrzHI2LkL8G14c69gY7EuN0+Rc/9+vk6YsIB4nhBIOvR6pYX1GJ6gUKWYwBn/CZBZkUxWTdUJ2d+3Xts1AwncYkiLVz5syDjRbKoN4NjPU5RWUnuyOfnwwi6NhUCTmftlxhmJfYQ5HR75GNb0lUTMU2x9qHR6qltYHcQc0FWdXe/Axy3NBzdwvD7x+t4Wlp1un7SMPvp6wQfUZHZe6TDjwr17imUJK4YPAcc9Hz2vb7QyxxHFw8Yh+CdnLJkMnaCEScelPLiv/lLyPIMkwSonPZRXuq/XP4gXOxvKe2D+JhFKjWa0M4x61P3/Z6x7fA77F8bewmve8AvF0/dygHrRap1udGblAo6E9ByzUz8M9XVuqikFJ4N9tx3VCqDN6mCNBVk/iS6/orxH4PAC4ciDHrxB5CHxJiIQkEa7j/UA8x8kFvdGIO8sPB7FbbcIwiCWrJs52TZwDLs/5+fZeOvqcYuI/1+7cdYP/0hpW7hEhqyFOb0iNSHVXl+AeWgVrRfoY6BasretMvYrLW6SIeLwnWrs8jz+3IMj9Rv+H+sPGyOUT6667yKMZxI71npQoyIIUMwf0DSLaK+Ym3uccHZXhnGCtJAnmuN6lKvvMfopvXqQW1ZT7CfF3rZF7SoWBe9zCegdCVzcD+FkgCvBur8VzDskA8o41LeGbd/iY5+r0RLkJ6J6gn1sb8gexILpFYcbMTT5LjfkN140jHT/G75riYG+DJJGeznHdpK+u1aZv33+lbYOxjPOcdIkPnnpB9jnpWndMz4rmBAL1A5gRuIR+X3fO831qw2Je1gY2VHX4OQOocMkxcSTFbxE1DOTR2ZY+hTBxqZM5ysiE7lpD5IfMW3GPe5um2bR8dFWikdnJtZflaLQErmjXdzCvBi9Z+ccxBRhI8I5+9v9Ss0hUE6fLSfsc2o27Bb8fq0J78D+ZYERE2veLNbE9i+FjlS1lstZjVm6Gvw/T3vAGu7bj0ygMBkP8SEgwSQwbscjqw/1KZjorBmZeEIS0WW7tqVExb1SrdT9N5tz2QzLGGpK3kWuhc5z9AkqA8p8AuwKHy7qWZcUxj6JhLMn+jkgc8JunaKrQcDmOMvBhCiLRMA/+xYdG59KoYv3S+ADLVrpTE2UYwl9wQT0UaYBz9fyQL5QQjj+Esug1CSviRDy56M6wwiNLNEELhe0YaCd6D6SfUZhkhkowERHHIMq3GOHbLyyrTvXASd4xTTq4scGr6hBtLzmeYZmgXXMAgQkghyViM4P5ywbF+hmGMoqGT+nRrYR8gbx5qFFo1d3LtldlZWBT/v3LamRyWOkfod9hiwCWL0n1pK7ZpNgSkOdHx/bIztp1XOhFvBWhoaNab40cyDLQIT1xGnkwBzGy7EY4yjNNOI+Hhn5A+G54QeqLDcBqCgw/S0QcMoTy2qSTK2//F2/dHEm12S0qL0Th/YkyfWqJeBq3TXFNBkyqmK0rYhKwCw5MZlOP+M2Ix+GZ7cc4Uukl6k9/gYiZdJVsYmJIbymf66G+UX7AKVNnm8bIoBuppbsBoxPewrCTj/QUU0QyxiULP87x8ngeL9VaRrzca7f7RibqjTh2KcfxjiFIecyKmrfQaCcuXyOaH9X/HFA3x4JL/4d1lb1VIWV3U+WRWI46Bnn6+ETsoxTvrbpRqRI/1+lRkcHv2Ts8JJnnVVFbM1GWMM/PVn+BdNqlFygzfFupmRiGtZAv7GBasy2V7uV83TVA6AE8CFWTKlOmKr6FYFKUk2SMRvdHwNe+luwFPEw/vX3b5VsdFL5SaiwwRWa6xbu9IgF4xmBaK5EUFbMFs7QkXv0GhQU6WZIjEBwDdI6wFyNKd6oiA/pIx5N+VbL9PUBrZFWqcOqKdoXnEOQV2Bw4hTh9p1r735Ab8ZxQNoIFT7lA99O5i3c6aFGozMsTJ0LzbzKBamqdquigVGZa/Ys2XdhKZVtn4LjAYh4bgeqGjbWIBh98yH/QKljvIyXAucXA3mVAZ6q3He8klWyhtkTuCPMYZRXcU6sUqiK2jypOQoY9HdslBgLS+hbznmaZICk7x6MflgbpzDJy8Awv6JsgZvZeNkYgTONKlUZvXmJzapZuCtTKI04OeoUBy3zMuN3gSrq/LhcvGV0K/poq7yoYr6nX6Xc41blYfYTyyc8fJcXlJGrDeJpDg3gTm6dGHtHl2DyAr4OtrG1LOoISmPIM8q732utlWuJke8z5RGbaIxac1PqENHsik3eESBSnzpK1UM0BdB8hBHvG/L6z3/nHgxYiRnX4fQkuZJ+/faJFspRrx3+LzsJtyzQ7qsXskxmR7UDerxbSAuFf/Jzogm52fMalxEVNp0d7dDVJoyQaZzzhQ7ISPMx2gYFJMJegryPJ8ZSZ267bmnydEQZul2xAftelpaPOMdMDGuMI+7b0S2BvmyS/oUqiQK2TI1eWETiOcPKmmTWLERlvhM/4AR9VJ5l6X66ZNntxlrMNBFm0naMmJ9U+5AWgObIR+YO6RTWZ1IRiUGRk8otuVJ8f4QPBJ1IdDOef6ktzhnM48hSnE8PR482/d/pWveHHO7cnkfjIKBDuAUXFJcX2MysWc41Gwj6dmycEAJC6U3fNZRVvLf2XaZ1cxPja6TL9x+T6Xe5m+1quU/UMc4dByW8drWg9gPzEnlPujAa0ysqdegWzka0f83/1GmPTFwD4E6DqIIj9JJLjoTiXZRuyWClC3FFzCCsm98ej1VMX4hUSLVsYxbVIvNClUSQtvNLq2ByULUZ44iXQ8T6I+WV4SbSDuU8+hg9dckz/9vlLpVGLB/0XXGUckdm5QDPb45xxs/7ZqYkHlyCLLWKqXXLsDXt5pMu9hy2VaxbSlOzKt6exiawd2Fsx0835Gl1IIZWlSTaHdLz7k6MejpxpT/g//M7iZhLkKXiT6cnl1CmZG1NyAvDx6UYsGBsGNZWUZkYNhGyebUVzCv0zv5KnRcJWr0kwMPcKqyRFIuy0FSOZPk/lT9KfN0x3deXcdw3KQvda1KUVUAAmCKuTpZPiJqPNeMpFiiDGfjryAWLqnCmzakWzU3VNs8yCh2hO+7QmXL0KwFy3XNu8hAuUPkaymqdaYizpBWJVGJDrCXW/cwToIwTiKDFVLZL7y3KJVNMyCz+9b1c2hQnO5QTKeUoNR/AMMtK7xi22+5Yj1UEL4l3j5eVbuLAPsOsynqICLNwlnRkR6xLo5uoAOF1SHi0FAvHEXM3kEidFbVdrtTrepRBUCLDd+mFqnDi+Cj/l8V5gULyA+IRZiPfQqi8nHWZXEJVlxVk9hYrTuUDlQD+VOmdhA7MGABg11qJuM558Op3l462NOoGn3uncAdOxS25mvEM/BsDNuV5epJQTReoYJI0j3mWhL9DmlkBO4oj2sXHBYSvcpCEwESlK4Nb5lorG+cdxcSiVNUVOxrRY06Kcn0l4hGZOM4drJiTEe1mQmSMB/n52Xj/nVG1r8tRhVLWfp1xalbqEN6evgqiOk9e8yAl30BiIYxNgBDTdJ6Ex1yjKyACsDCh1OpH4d4l28efPNkXoXyjEwcAp3LiotkrpktDY5lIVNUmEUCHbLNZh0GFk4ExqmsvDeBxs7qUb8PPMbPHtgvpNt15mSo5De8Xg5zJGIFOLAmpKy7DADFkv2zteI9EqIXERtoRG2GoU62C81j5mwDk6sxQi1SzWpBSQGH2IKi04V3WB2xohlRWq1tLEoB1gh7+JNfh5x/3Kwhfnw70zLp19PE3xanAHrd67Tz6GTgiiRHv9bZB0UF+Voc3TNYAMVHpOrcH4CPLuKQ7+DEkb8Q/9Za2VPTKMMGpjV21Yeou02YcXul+rryVI6E/Sk79Wl6faEc4hiLpY7RSh4nXN9wmGF2hU7iUpHD56gvlj/hbh07fOeUZcEb9JNfghVDxHxAZx09Uh0kiGpZLsynbKpmsrzn/FhNRvhmDnI5FmbIh4N2DX5oTkGjKGBkErWSFmrIOgk1TVLtuYpBlBnT3P9JvlDOF/r4Gz00MX+wc+YiXQvP+IPjx1xDWAvs7z3sKQ9FGysGaTvtldGXWeXaldVYVjX2yIoA599KMHPcgAHO5LODy2AaaqUjE0Zsy7wKzV79IW0OlfJTerEbAPShFvykU7gNsDdISmXivet2l9lyYZlk93SyuwNYMrIwTzcaWM9UPkjvQBDIkpVjb4KJtjAlxBtJPdYtzSRvEI9Vviyva7K0UjWdnG+hYpNHYCYmQU5T7x3/aUbAL8iEUEaFrtPWvErxRcU6hICPAPClU3wrBItou6p67B8sdPkqpJ/fU5gSxl1q5jKwX6jaSb6RLQhynTZ2iyiKDXEx8jR0awxg1HpxrkzfKFfKApTLMEkoqzH6bsLlmx8YG/seFQucb/BTyGTo7hm+AhPJd6CMKBdJGS7M0DFj0Va4t0zLA8LMr/D4abaQA3PTGcfbOXaq6+SmKXdssyX9tb8oq+u+IecALZmLCVHiYB2Q+lGKVAL9HpZ2PJvw0bDbzRZaEkTumiVeHse5K7TPYOuk/MAT8MtzZsEHvDTlLgwN6tGIAIqJnqj3+L//6uQztY3II5BHM0fQKpKlPnYrde4Zw5k6QbFRdpUCi+rlT42VYcp8PP6UpSiOAVaIU1SLGyNdHgQkgdMBTnvD5B433Ec2h2wTgNp5mknZ8bvIaipq4bJ8dCX/QdQjrZ0gugSfmQbRIrI23IPojGyHCN/qQ70XI8z3QxfkmzhCDe59NfTreKMOIrgG2TlZEuBMQy1BaL6gL0DP3MdP8tBXNQks780mlt9p38PVmlZT0ZpxhwDLYbRkKtyvm545y8hQYPcdzA8QkOmT0E8l8lFKZmb80yRkfYK4F2eLHZvPLVtCzy1qNAJZz1Wd1YN5JobXSIZVNbkz/fw72cBIqu1ymNfBajP3jdJVDUXCSIcrE8hyouXv3/p8SwBDtDqtJT0zwFuXjygOBeU1InA8w7BsxF6tUmhjlGeXl33+jcUoT8lqypYZm1PY6+ZfLU5R65BKzeU19mVTf549MuHVJRe5HeJZEehmzUJ8YzQfklqwt0ERSE/NFg7uUY76ZR4Wn/yDZUeoUw352Vc1No7jrA4xfd2bJXHyQYWpO6iv0SpVXmOvMSLc+Omq+NtLO3DaD+RiDjfFXo1ylVK5vFRSUTNyA6TW6KjgPuA418hILIJ5DjDnrQYqm4UaGd0EUoBrBys0eud844siXDK1HxTHXNEUNsEWPrfJC1gwnB854Z75ebQ/XdaIYwCDD6rAz/z5+N5gSiZi6c83BDcz7ryLHFJ9+2G9uTvhi8rbWCK4sMBzHSUehWHRU5jrqSKJdkqmaLug1AFiRIcrlwh/IxlWmvsZHhlXgSb5/VHSVY+ug51XsMVx+n0JOolpyDt4l3jvTKoC08nmhbXJQplG1hLBM4JtFuKL4daxjhkfmBSF/3gbu0KZy+RN7VuFmd+w6FEHzG9BBhSPzydRo7CM+Gcdqs7nHJaWCTM3jmkuebOkt+S4pPN4f1tG4RspMeX6vETDJHwp10nD+YcEx5OXaavwRD1vwWZalrUyYnFWbq+wv5BqHIP4ULznZAIyI2gb1KhcL8Fth/wwafcZknCngPtnXkBnSHSR0vzLftaINh+EGxdifJMwthV6kcFhk7nW+j6lbrzMdcMNQcb1dclPTD89uji/g1ONekwMjdaAh8cjqPezPEsPqsjmYdcUyzSsfP94n1+6GR+oRc1iQOj/DHAJyy3WGZYFqnra9OsxGQTHRS46Ek3L1k32FnPxanFHbBbh7YUHwGsPnr2zWSFNAiENPt2d+K4FFxW/MGtL6oDT+NncR9E2Si4Mrl+wi1+W+BdEZoVa1REJH/inf2aYXl09mC8RvDcBHaD/gWtpJuHO6zORvtTcXMtNgj7O0X4iKUdPcmzLyCoxqyCYODLkgyM63fNhIZ02UByPnYWAlg1ahCvIo/vbWS90WMVa2H/vX5QuL6THn3rwi4R2pEvlXemP1Dt/YsEXOJA5nzGdWj2hSKvYGzk+uXZqX1WGfYnZItgL8kZxc9dJA38OyL84Rsk3nCS4P7Qff/aBs4TEeOfVaItwfIFuLd4Al0nO9rqsB7y00ab1Hl5WAdujPAoaZ5ECHT/YpyRseNaFFnJX+Aqp1aXnWQGa7aUJk4xTsCMxun7KEMuoAPHqPPtDLpnTqxhXM5qUH/3LjBP44ERO3dKWg9EjiPyMR6l8h0j4NaeQSnXyGYqm/pDT6KTRJryTC9vQnjadCzqLkTqwnnFb1FTEEtlSImP84vF5BRvFYWbRnWgCwaP5JnTnyhJYnxRodP4x2kI2ucd7PUtburQemaYt9lktIeNEXm6SCT8EJBDfhPV+6WnAr6E6mQeA5l6KSGeY0BGahU8nX3CL35gP/y7QRxCmqbMs6NSKEWKiQ8xb6IxchzF0h6igXPZ5AvSyILZHg31m0dT5402GL6eQarJMA3vLXXYNM8DOYUlELikq06JNG1kh+ebA3B8srFWXZOctXlTHln7gYzTNzMsNYi7eUetnUM/LxphzmBa1xrB4GOd4C25/PAbhpBwXMXWLwb00npEeRIPcT4sLmTLE+JGyLe+P93C6chVza74sL7DTJb8giS3PZL978rn7ZFQFsnjsrsS4XfMEy2nmqea3c5F3HUxR3sUePhY1Z6ZhIlYqpItwhoGqiVnYwmUO/qeEGp0EiCb4OCeYXAnihYLsq9wf609FWo3FrA/QY29X1WemYRMbe/WbCQsAe6icXNpBIpqfZLZdzERzTQ0mLe0cQkHa1VLdhkLu+JKRyMk6DKtG5sWjCwybW7q19xzmmQ+ArLTrePrGkxXPVPQl8hSpaoHpWFZh/v1uHXKqLr06AWW0P71S/iuMPnb1mh4viIYFRywmid0F+1Czxtcx6/iMPGedNaIhSWRiaTIY6/QTCxO1MrXhsKf9S1PSLeKScfae55jr4N7JFmSsOPdsTh6DIL6hKeQnFYB/YFXkLtUmnA+JGkuCgBN0tCU2KP8PR5UWKrXKgmO4tzTyJeKRjSGjOAOPAl2bfDjopx1dqhHwIc/klzHi+WYaLsQDHBh1d4GqQmqhf3qRv79ypEPcZiiPfIBYpsEfKybRD5h0SP4g+B9U1D3DAGdRqs1K0goIn/QdFB85Bm5iPJ5OWVJOQ6GHAL6lcnFV2XvgB8fSmErhVSECNOEm7Xn0dwyviAecD/NyULfA8flbnZojh7E3Z3BHilu9JrCecXf0bPz24IeDnwSHUMy870QB5p2VZYfgC9Fz1P/vA12qIBDFDtB/T3+s1vKFq6/yZM5NJ9U6qaxpE5A+M0PIAj2hXZYcHdo9CazmycvoZ5BW/ip0N7iQlVutchZTlDpqDTb+G7HOhM6UevW1mWMkn7rLTYNUwDDvkdFazKD9gp0SFZLNs0MTFIvsoDE79Urqtj2/TqTrq5ZsB3AGQL4VnQmb4HffiqnT6Jg4C/GtSiWlKP5tCmAbfJNP9rkfKTAJCjjTXxboUoIFtv92LN+pn0BnSOz0Yr2eOr5F3zClRO4EML+c/FmDmR50s6BPS9M91qH8+apQy1ujKC9nhBNG7kVK2aJVnjTwTLqpqiIn2INsIYVK5Lh7EOxRrxyDpWbpJ9MWbKr1XYUj+DMrbrEWYlXGJk8wd5gm0bM4gWxO4Q8jru2bHV2UMw0J5nmRqD6Rs5U6ub520tzzwCD4Y+kqrkKBMwaN/oZHzUaR30yb6DS4NtlTf/9c+k1ddXvdnQLtuTD2leqsA6Um+z+R/tzUwSakiu9j/IK2CQrKlz325RecAwxQ+G7hEuL78KZliDXraCSTqNlx//D/WM9s7y/DqdLxraxPNTaLM+A3a1weG7LcN9wK1Q5VVdX7rd/rvklHodWZs3xlq4mt9Cbhx/VWWc7enghOEWGdU/EK2kfUekPdk4IOnftsBtRXmBXcy0R+V0fVHsCoVN5sdZK8tFD/lF4A8xTqRv6od10FANMlrrpWnXt66cq+Y/3mNXeMQrVt7Y9wH0sS8VPRyTXmOCW2/alI28RPIc49pgqW9As5bSy7PI+fS90HW8TT2g+d4ngj1X75LfXjDTs+e7BqqIQBqj0lzsylAa+dHxiPQe5i7/ByGWBMxjX3thPdXgatl5d/5d4RbugT4FDtkxAXR1Oob7C9YfI0FOPwtH2DrVZ8v1ijZ9eFbmEAceMhh5cfgG4juN+HTrDDPE6hUpQ4vKpwcytakDr55THzKWWe6IVV85wbLbZUlmvroSZUMBDnAIfvLow3QoGntgqUuh1u7GLsJfGiJFprR8UPjfBM0mUo2/yoXKqxUgHyfY4m941GdUw1+kzzh1fYHj6Ug596kIMUSpVyiRCk5iVPFzr5Z7WtCZpcfIuY3BXrxTpQyx3qSv61QjFlFIog84s+mEc/1L+/Au3HaQfAS81RtMJ4T28L9QOB8HmmUE2zwcxA0vxaaLdh9z7usTIcIGDGBI++N/1+VsnGo3b07xQr3AuQIOWXSGMrfp037f0donAwr5DkOfrlbgDvHIcrt9UqGEgRnjCyoiq1WxaN6rJ7hfYJe5RnoQ2Jn0VGHm+lD8zQBMYcUKvdsGDGqS4Yg2GjXt6UE2EFJdI1stobuRMW7IPWWtTyfEPBU9Uk6fMxTiZmwAfU9UyyBBnriZgg1s0ufY4B8lqL8SpdDU2+JI+bI4B2QtXznz74/wg+zRr1UdSudQJSEuETmLAFogwUl4yMWYOEcxjrJL8+ivgLOW1skz3r90OEOxaMz9N+4JN1GrhztGit40FOVxKZIpWkDdtleJL1rBiH7DNEwxjXRoeMGzURSIZNm+ZvtQZa7P+XXqW+NWucBvEtsecsB0oz5GLJ9TmaLQmmqcl0grVWAMY5viKO+GdgGHGGGaqaOp1yVpG+4lKgzwBCuSrZWfWDQUYmO+lH/OQBogwkv82lFIb4Aln6df464oVDFXEwv2DnrnaYci6gs/cDiOpIerw6sETYkwlrSlOZT8WpSIIpeJ7o5WizxAYh0inGZ9fZEh0ldIscp4tH7F52xcqqSrjXGFqhMsFB7ZtZWnoP9FLp8RS7OS2G8Jw9+/wLPc4Z9lLXqWoFfA3+UNLOaskXXsG2ugr550hi6XrhVNX6PQ4qKuUapfQUwwggl6jgBJawIgTeXZoX15gWYQlR3wmX6k+JLnbJ5+8awYd4Jsk/zRHAsmkacjbFX/TgWPsNOa6I5EWDhHNFtmGOKq/VVlEBeIslp7c/oE4DmP+nbpDjHG6BcrQYnIpQUwt6sBrZxRHTCUW+yKV107w7DZZ0tkvLgQZ0EDDHIKfPDq0fT/Xi/jrI9zQD9AP0bd2jUEt3PvVD3MBMm21N9uGNfYrhNlSLVJtO+4AnVHhl8kHHimr9Vwql44Mb3bJcAs0ayBnw5ixLMjqpM6XMZO5FDOaAiG23kE5gsjy2euqhVlEZYZ4cl49XnDIe+OenXrSPbDKsW5gokIZxWhJvpQvI5CiDMRmqpcUl1+BvNfMErz+7oFMgRC3aGK+fU/gXP5TvqnuBnlQKjXaBTPzmdRdGNplHiPxE/hVsw+T8XJrV//AyhDvzx0nauWQg17FLZ8Nxq4MAHnbbEYYlE/xniEzICjkSTleALhXNddYgBLfU0HG7jP/ZUhTiMqusAykQOLp5l+JO3FsW0LquWsTrJSKpbqB9pep5Xjq35UuIlED/UXnKsYF5i5xnDP8IkxeLxTYZcAWOTNe/G4Vad7jfz3Ls7iAv7COgefnSLWcDAuxG8fEsjz0Vprn9WMKtbhxj4Gt6z80TbWE5q1yW42qgBh/dq5o2vIYRe7kbkACNgh0rG06B08nRddYIPNfEgD2TpV4M+zXGZr7oMwRUCcthotYq/VNG3MryU92uOX68FtVNjYZBE093uGbA3XHzdWCK8aQsqplbcP5puiv62U50UVXDNP/WW4RrH7ye9iPJ3yBWmWadMYT2KQJKH/xWjJx8wxFRzvGFWJuED2GOfeZK1rRLeSlw/1HTw0vUOnfsi9Ma5JdoGvUGwGzo/iQnfw7Ebq2xZad9Mcq80QGnyE954gDCP7/1cgBkRLNU07t62S5npdvSftTubRqYP/EAyIcAL0cTnV6U0DXyGU37mNF5j5R3JNdw83OvrUtAJE26eM//M5h3W7CT5zqkv2wu1RvsNIT+BQ5eHu0flLwJrgAYm4CAVY+IfxTnKLMyhvQHNWFgnzHn+0+INxqAw99y7J95FrR/uGSh701CWx6VLpmFSec8eZ68qFTK7Hpck0SHGsfEbjVUVMI0rt4z9UdT+Y7bVogTQRP4N8QEiP8MB1cX6E6RpVnKFBS2pbkE3rE6Wa9R8iri9Gt1EDT7ZaLLK90PasW+omu0o8GTEMdc8O2fVHsvduBGlY1d6z19/+DgRbfIQhDLMP5ewpxLIAF4qwGaqhewZkrg8+86yLJNd+B+iCHBy0QrF3u1TsnhQZd9AJfJkTDXzV9k6nCPN/fgG2wJefoxgpJG0ApSrc7Sd7CrIH6la5001N5RPgJuoFvc9FSCaBWC3IQlwtkmZJphthq2sUJJPEneAJ/6Kol7Zvzq0nP9jhlenDb1ba2mYTNvV5lOtQUpN83BLrn9GOrZm7wm8atvdnHbtF1R3tTLatcdtvMIr3bXgSuwU+w/0FiY4iErXl7UI9jcPb8cWbvk6AzaHK/kN03yP66xRz0lQZ9cmsovrQ5/mfbHa+yqKDq8ZuwNxM9ILltT0QbMrQDeeRzykIg86tUWQJJl/lbXpVZQSWHjOe/TK6RWQtlCBvc9X9n2KW/paa3/LBc6Nrg+gZV4liVUt8WNdO79PgH+AfMS2/x3EWU8rw2G+yeAWz7cqr4K3Ot4LuF7hCydriBCan6hJ/zoBMYQPKL8/UXPtWoYh3S7dsqwRgwtNbZ96tpmzSti8eaPF5DmZVqJXqEJoJMZc1tPkBbN2TX3IQ2Tzdh0/oRbKbZFikf7gXc9EByfVMP3I/BTNvS7sked6h1/7RrtQL2aMVcjc8Ea8Yx87xlUhuzYbLvJW3nquD6+p5QafRxIwgXOsssd62q49vISxa89H4zeWNjB8lw3VgPQFqmJOJdJYLLEwCD2xToI/yWvcu74Cw0gJPd1344/8B8W6KazD5zaTEvJU90A3cJEGhMDjVaQ4ViiFVSq2MVp/rwiAZs9r2KfvCNFMWj7WdKvc9QPaqzX3iv17n0n9Xf1da3XIV96I/RDucB4ukBA36DMOLfdDjjPNb9i/qhCCD0gvjX/rg/EKyOQ858ioLtZStRbyUXZyzQPOkO4E+mAJOYcGOvwpBDq9QsYkh2PA5+Nckl8Bf5Vr+5OjHZygZrOeoCfYXLYU8FN0cM8BzJLsBvhmDj6AAT37LgM9ukXBJYdjwOf7R4AGRmWXcu6Ht2u80D633fx3wBy7R7RHKDaLGZLToQPxaUVH7C0gtzpQIO4LwXaTZt6q6k/GSwlurl7SzLcZzOZqk5i7YdVevG3MbBwpyUOdg/sL+GMcGbZ3DpYHJVfbOeVZrVqIjsw67DYhALZQute0HMqmOsqilBn8JJIykjIzdYMclcOgQeAkGz7DY273ZlUytEqefN5pr9qObfBuLg25SKXMr0XA7D+22Ppk01m+Hr4GdzeSG8zSt1u2ek1klDZNwkshA50qo1//XOmZzUqrIGFVohbQ7sY3hPBq79fiOpoS8lv0SHwrnAKBkLZQojNRdN1bP6EhHmypC9MylinO6PsdnxdTdMY3+pXnR5Psd/GdvmTDTKoPrxhvL8xT0ZOyAfNnBCGfDCDETS5LhSDvedptrNOUJK1zbRP/feeYp0vD6zjj1IZd6SOfYIQ8S0y5ZbCsy3KFWiYX6kA0qn0AIv9fkAalEtOs7l7XFVYtzWODgZd128Mw4PGUGLxd9VenUlJ75TOxhdg6iEpgeZsMN8cqCUvKLsdZqmGKsfFl/HprF/JQ37HDavrdEtDuvmTQXrtfo0N3Y/Nu8LTRO51CfQbtfVqVV2lchCSsTOVKv5Sfaqh8bFOkCc/ji2T3yV6YpsNZrWeTZplzWRWuYv/Iilulb1Y2zQdor3gNOOFNkjPQZM/g8geYDU1hii/Z85M78Ysc3PSOKtUF8VHtXCM+nVPOjrED/TMHKMRSeoBRZx2hRJgtmzmS468I10oJNoZ4vIezSv7OFsfpqzfDHelL90M8KZVTmozNLJtTTW26Oh3SQCoXzXL/EO0KwffvT4lkYxf0EYn9iz3qnlGQp9VriUX4AeUFNRSzeaXw0HqJDmcc8HVZg1JbP7JtoBfgVP/eiRyBHwF/mHWvm7Jclqh1tquKR5Ab7D2cPA0Mq3Cj7Zs5n1tuQJlOIvExBnTlG85d/km/k40oumR6CsBmqJOlG8ejT6+hjwLwb4Qp0zoVBbc+s/nZaZ0NYx23ZR2FBGlImDC+Xvxc7JrTNa4jZkTwBZT4jyP+gR2Uq9FU422KKfk9RgHheICykybTP1E6kk4/pCFOHLFl6nvffcG39RvQAhV31XL1if5bye4r7N3oMJxB+hnlRio/ylXWkbAG4HoQZNkIcpkeYEHoStYwkTOE46FA31ZjQOETi5fjXoz4JrTe8GyYB6ZdrEhobc0N5vqPJbsjIgj5QmidWjxEzz/kWqZVs9eXebB7Lg63HNHlhSz1/gXwlL9mwEqqC6scaSDDVNzc4iu5VEIpgUsxqTNaZN8EknDRbNj+4EGeXE4oyWykja1Gjbdu9czwdYtRrUS3RWJ1xxuOjusOuWMWf91Kc61tXm+9DtR0lyfZt7tK1FJkJOEEyuLrFpC2eI3mwQzZVMJiyXh7Otsyzf/ba5oGa260Y2yEBx0zv0eZOcY337v5GY8JEmHDMKzHvFPVuknA8MVjzwD0Uu5aJT7LUNmX5Ue0JU842Ax35GEHZ6lPkyjOH63K3GGneHkJ4kOEsdo2vJBXj7jCTLF9yWTENxAR5CTA2KdPsX1XN55LM6gtR2W8EJt72T2eq78F/Cs5TKcJkPibQpX5P+rVqSyADedGogEmIp1TnsC+VKoyXyjGBDr1KAVVij7gXKVTpIeZKOk9YwbsSo64kmPhxBvJr4Ra+jXBNNM6GR7gIPW7ni/dAn5dsDgQzFVhHMlr5wTiVraBnC73YX0Cu0rWvY0zspZTj+nLFrZ5jXmEc0EN53G86Z1swwsnTLsxRddad0LPK/5NqxT+0p577SB1E/JYh7GWauHFUtOx1BrsaIghxWZBRfo0+afZM81TPBmnJwDfBDkawHS5BPpY74idJ7U4fgyuW8ug0n2g3U/JpIZc+HeXP5QmVhX0buGqjj7LVD1L5TlG3V0/GsRo6A7oXLyLliT9a3cIsUrX+5tn7dEUxq2MQaRyzm7ObkhQviaprJt71go/H7dhDdMIPR7EcK0Wux+ums17pnJ1F/1Xw6zZN/XZBt7kgUS6bYIhgHMXA6VmvLmFbsNXPUimZEiXT3UQ1Sv8E7oa6Y2ZP/wmIx/0Wc2v2zX32wTc5oNGuG+AJ4d0EASiYbu+gmnEUDxIpmRIj1RnSZIx/gqvDv37uU+kImBDpEGctZZ7+IwQlbiNU/M8qgm+fwBHpWn0tJAk1UEoX7FzCZFTTGyhdPATskPgktIwrS9hSbtelq/QLaiFF5X2gw6nM9B52z9QR60yveOUIdNMO0rgNx/WVzQQzWrqAKMHs8OAYPd7OhipW8Ko136q1E/GpNQav3DmRfIzTAu7MuzyjGDieAc41Fx0p3xLGcJ2vAD/G6PU0yb6LzNU7RrFuc5jtoln4J7JHL5kkDicKx0CtG2z/Z9vwg4iAb9rE4gObELaIuEV6BXzn50g4C1wFuVRxe3OILaaQ9HvkRbva9EilldGYoxAmM2/FfA0DWXbDnq2cVlsqlaMeMY3lJDTJeczIxzrRoCsxCu4hmrskscdqVGwBeQRJyKZC9eC9h+zcmkcoTwBxxIwTMgYkmWGepCk6F6cRnsP7E6X65Uggp9g6denacFF/wP8GDtsiR+V0vRJvi9HN55INKguTWe4G5Bw1XPOufwZgAhLbNAlvdOsAtCkareBtDiHGPtWsll0ds9GzYP2G6tsEHiERj+tLUZnqgiBYdRzxcaEcu8VVWHRI7rSsRrMtS3ftoBZ+QbmU/dPeS7MXpGHsEfvJR461kFnnUZ5RPFRsw30Od/CwC7qMiBTuxTc5YUs9doAkvjWVqN0gCGOSVpqhh+V3vdDuSVOPpZDPaQjCzeSUq8xjC6F9LdK10FhOpFi+o/4BI+0bqOZ/XCHX/4I6UNycIxB1cu1Ur9vVGWYGjLrcVk+t1KYZdpyhLazFNNKAzDXZrzE+TrkjxiRi9cH2jGpG6V9ZC/eTMrov1Hqc3l+twMS93ZHAZtTjRDOaJqUxzivJm9c5RvFsL0dnpRboazwIZ92/Q+kcmVn7TXf7rJe0VosXfEvRNNaUAWHI6osxhj7285XyCEqaokFn/bYDcv5af+Ztw7KBoFDgkU3PqQpvpCjRusrBTDBV07GXidA3Cj9Xaxz1LrpSIJVTzvIY6mAqFXF+Dfi8cAEt3fXMtQ/GCrbWMHbuF70MQoPtQp58XhEIKpwjxncNvLhwlyycU591WvggLVdzfAypMX0IYhb2j79Hw8zj0i+74U72k4sLuJ/WZRvAXDgPaZY6kXw5tFK3BQiXoIyzaekasfLLP+RrXLTJadioRM9DbdfhqTxDPctEWetJhfoNjtpxADsbrdCjpyvMsU7BVCZL8Hz03qolGaou4Mm9H3KHuQpOnrFKNvbqGPsFA8I6joH6ApiBLVFxXy6fLHKjRPlblpkmgmRkr9Q//wX2fqsNMNOt3aPW1gYvCC09IJVwhwVYZVHeOAuQnrTG8x1zhPS1fdg9jc9aNRHqLyWWv3QHN7EnTjqEpJ1pnN9WMc+796IVsEgQzOfIzLXBTEb2CXJWplNp5yZKbJ+JlXobpG6j3XY2QTh76UY2FjEAMJyeFykTMSF/U7dPCIu0nN/4Q0xDdMRzE3oHu2Wrz/VPw5M/FujwcNjyMAO0M6bO+Vq3DrsJA5L7DvytcwFghsqWoNWTdY6JwSjB81q0RL1zdlDhGw0TqAJmLi2WPTwE8vV/3raMo1xpmJjV69CqKPLfohiT0W8OjfWIRZywwX0UZhSp7OVcbRdZx3IU7iK4zDiml+Ci/JLtiSfe6RVRX3pHv/8wg6cU0ZJgzUVhgEKY8NksgnIHtLCgiDcIQtwuhSWmaxmsYl2g5GtEatC8VK2Ag0Ulmyz+IxQ9y4YG8VpVLdrU3LJN+EErXeWvZ8ahQ4Je4wChLqYMYGvX9PPthvjOblZmV1nXr1VxdyOXKlmDQzkdnmWQ1EQvEbLS5Bsq7uBE+l9QTX8b/LswT6ChBr+87E2zzOvD+UlCDTVLvS/32jmIA4b831ntzUJcuNGz1mZOYyBxX6ZW34c+2m2uZ1Q9vUF1saTN5YWtVSBT1wdpz3BgqpvxBkGb54QboJ/fRnHG/tPj3y1gKEbwBEzUacqyt7/MpS1LPrX9FS8Q6VXkVcsLogVmqDyJ9IIZRHvU0qpemgrgXugGMsby/7bZYZ4JGDTVq7AzwWZnVy5268G1CHFGelDOSaPGe75nVesSWRwjC1Vr2kdQOkN10CeRICh53+CTgVzlRP5gf1H1/kB54TfZL4l22nGNBtT1SDL9MoepEpVK/FFO/YXAnXVE8tyiHDE1+dgn25cJ+gSi7m2Wda0WL7dqBS9asF+hlZVZtMf3OOKX8hSYUzmNBj4OCFKln2DJ4NSh/TAa49FUBPSKLK9zT+4iXeQoJgz1CzMEPgeKxPrdIG/3xy4Rko85UtKh1RbCax4hXyhdNrI42CGbnkEsyrw/+s/48Au4IzdYYNp+Ua3d1l7ywvy0YJ+0S0FGvVGa7JJRTy6X6ktyjySkYQh3TUQRYUc7/OeVIGuTraey2rIQeU7/xEXIMJekqacK60rKAXYbHeQTkEYum2AAcsUxeHGYIxbeAzLapKa6jqujXSLhtN/3le0FORQOQOcco+1lyOWcX1QjC5WzwwQMa9o51KLTJG4ug7wfWUy8nW0iZ1X0NY6voD2T5JczBC6en1U1A/d7KhmyEpHatl3CtM2KUDOOMNejGm7sK5MujQ9asV2huzsIKuIbOvSqgHfDZJXl2FGYYB4gKbkKp1/bWqmBXuAdVYjr3jqaKpopaC1HvR5UziFAdjl5zWVimWVqYtauXfwOM0jCy65T8XnxAWHenRo321OikpeG4RbyVquSpySoRr3HSQHuy7/joteyuhyvITWc7hy5DbhSzgf+HiGzL57iWZYaYggQodYUg6CdJ8f3nSgpLsm2w0zYK0i6MvYN7ygP7ul3Q3EDZRG4jIYWeEP8c26aMcqRkONLBfHQitK0QXpXo9ZiY+KGPoOMEeHCZno/U6dh26WmNkHrnzrK+paXW7bNsuT4BScdGRzgFR2nWx4DbNOs1eEQICwu1nEDQ1ZiC7G2MsXh49wi53oRJgY4SKbKTgKlW+Gw+oFg3pzAN17VLxOPk/XDf1lpF3owfFnh1p/AsI3tbq5E8TYRJqAxXXRMKZ8pxc+Gowbj7rgHL5Fa1+/DiDyIk8Tn3iUDccDrZm5W8MbGHi0PcX0gnHU2D3v4p0xlgSDVvZAVxCpR6qBpXn+BRYC33pQt1NGB5w123i7TpqOtibZNCxWmBr+94lJ/+JxtKbCaaxtxxLnNyMDnneIsdQAqlNKY5AFCME3NkzPEeRDllCYsKYW/XA7ZadUj6y7aMbrANvJogfhaNYzgzxcEP4Q/vW9Xs82GzrvKUzERywO1nT9H70NstKeCPcvOXqrOOvgwQvX7C7XrpFbpXfGM+ZBOWqEFsrsh1L2DW9bqwJp73kMfPoiuwzwBe/C9AWQCQ5ShBWEmo9dm/52gO6ELswRgH6cQUEHh0G+p/svqXVqa58LDNAuIGDJAfFsqXTH/8MmzBABRLoAnfeFKYjzKcrmjDScatMO/z9NT9QurZTuAekKIwPVflyOWTQTmm2BY8IdoLOyKOBuKmqLJ/ze9wuszifd1qIe1wmxbpIlKRShP/bVvVrLMz4c1X5ZyyVIE4F1lnDUAv3+5kenTlkt0yfNweI7iLBexfSSEukhthLwRUpO0kiwjN45sVJ7aKQ2ULZofC2LKtFonHeWpLcnvy81YJIc+efUFrS7PsSo806mXLpGm1NVEpBw/fmPPJ1OYxHiQD3WVn05pmS/VK1YkJ2pL/kKEnu1GNr19xyoo0aBrc1X8i6fWok9MhKQDvvvjj+LEyYwkRo91S5DHr5csTvCKubK9GOAejpJnyXv4PcYn4dosqTTDeQqjVXzRkFK0xTd56RI6jkNCKEBCfAsMxiabp8n/CSVhsUuyT0mfbYd0sPrAI+XS4eVwl/sb58y4RwRIoJ8idjlQ7FAVXqoCyDjESdXyRHvcIl0pbf/Fe8BNH+QAP3Q/z7v7yjF7bQLwwPoEdooIzunMbqBwhSvU00/z2htrnZHDYxlsTrCGqyiuivuHFl9gCHD8YRT3rUls9WHF8lJ3xzFYgxf9AHK05Jv1QoWCP99W75HJUPRJud5s3LPyotopCkuZ9tru9ChCY6/W4eXxUv1J4V0hFZeafIl69aVScxQXmjBUX/+Ezp8v2jkV65Ep9TSc79IelimNNGgrVzr5jnph9BiiVbdf6VKeXKVD4LA802sOAkOwhFvvUU8A5Zirg7qQuWauiG2R1sb2UukqKFwxfoxytv4QKRU8TKTXk51hAeen+sbvXlCdo87BskaY0qAUrIx5yTn881XqWR2KOYV7MPMI5TuDOr7ylnyaYZXs29JAatXgMODSLhZUFzmLhqSGwVkzi7QY9wUuoiqMahKASH9SICeth/Ot22OgbkbuHfRLYpebGvRUYuq9ETDJRlnsQR0pEZFJ7lximC/QKuejiTvZk0SwWy2n5NHx/dvma3Veo5fyTjGLBslwFeAp/cdt3FObZsXb6QkOUjBYrZWsXWDj6gr/n1kWukF4MLUOrCMfuX7pAP1NdACwg8pFaE+p+7dZOInLxPfakChR2YlvW2VE8Rmoqv4UMVcEj7dT6ewkVD/j0yqnb4H2VPJCtJ1G0imaonDlXjUKxo15npfpCgaW4NUlyfwIOTn0UiUQ3MRp12EkeYVw7lqkIf3aIxx+gDTMCo9qVWav5d72Qo8EbA9Na1ffA22apISxx/gzvhfwjc1QakBxaeYbMPpBsfYkhDqNrxovXtNauAl1d6jZp1dRjPtflW8RV8khF+RL/wfqKurHcgYWXyBLsz13DGdt3eFu/BhtzyGQJN/dnfIMvPpqh+aXGRPmz5Oo016BapLwFS1QpS9j2i+V20f1WOSmbVs7ew1xtqhH79h0gD+Ok5WxFm0gfIxtl5gY6EKL9IBaDKrdfpDuhzgkq8f/jAtaYcg6uj4J66NcYS1x36Da4B5phAEJJV9gbPoK7JMelG4bmG7agV9pw/PW4JzpZK3AMVGUBnydpiouGnk5j/n2/x9hwyIXa1/eUncNsfbpmHNVjgP8nxemRo4R+Y65EOLQ6yWggnINHUWxD7+xcs/vMEC2bHkZZZo8SCHR194x1qKy4959SYXFr4jAuI1A2XjJPdVoGq9uI4o0Q4XZ6EOzKaJRJOcQJaK0nuSbvYP8TcHRNYL//aMYYlZSkeST3ONX24ZlF2PGskv/PTsXsMUDGqHILmllG7NyCPdwIkv0ga4GtImKyyUCYaM7SCuf1Bekx089RkFUdQ020O0bdr0tVOVaCtsoQDq/fo0loV6oq7UDs0GsXaPZxIakHOrm/8jsXJiQIAsIrpkaU/AGtRqvx3x1JYT+SAUQIUuwcHtGa6TC8/lky3XA+kA/jEQI4UZ9u/GJ7xQTUylF2+iXW8QuR/PWPsv0PDodJpoXAe6Fe/Dt2nizg3SyuBxg3bHZYJpemHWGuntu3jJNiYI8Vt+vzoIQZtMgzORSo68iBHGESVf6UKEu7pJwL9skoDeBOBq4hjMKjAInHC4ndo2lGheTawhOqNBTTy5ZJwXzwfB78l94BESZqoCmbmGK4aCX56Ny0m/YOo/6igBJp1agJnkMcsLIVWbKQLFPCZZ9zzHedsjlO7uWLJiVnGMfp6JpkvrwAD1yJNNm0v2MOgHJB6hX9zGlSC1VW1GnDkA7QMbZOUAiz3cK+zF81mPdUo46ly9sZ1p7v9llqDfYcUVjC7QPgsThhn01KcRkHgbGNpxVL16E0LaBIkw5w3x8cp6jEICSqQy/f/IF6SBfYOywHKPY8Y/lCElIpN7grDJCpN0Qm2aTHKpUn4Glz7+Q59ArJu+C85FUBmuKu7ezjK8viT89t1ciwCEIdE5NgaPaIm4xSyDGBMn2mhKtzIQc9Ig0nXWHvH152y3S38byVydprBE9YxPzqXgTL9RwhPpKTEhngPIifAbvXlITf5jeJhPWT/kFsVnlF6TlrQS6x4KeqQL952yTpqFf6mfyGGxQMgJ9zEGRcQE2viCQbBgdHmseUWBVGUgrGWlMPcI29/Je4RTV3GcDZSYsUv49R7j/6Y9wCqLKfYBDEvzNbqwkVnXR2gd4W9kqkZpPZZznAvxAu/B5R3bKmotmzrE39gauLsh+fWKUJde6TLLIxgQp0Obqs4Ss3BCYqIQHoZYVQCAcIY4mH2RldRRt25wJuNEqqqlUdjheaqD9UiyTOQN0Rg5A6U50MmzUconOivebGOhdGcYwCv7HLxomrqMGvQoE1iZNtjpnW351RXKwuh5mGrbHfoRMCuUX7yN223EO1l2jy4L5GZUdq55qRnKFNDT6nPqPSdZ71yapahbjfEi0MKyLso7jHayU0lo/ATU8dU2lHlPXLM+H4VnXSz2LdVvunKatIYgvVRXI+pC2buEbMHrCcjHsTPsNrx2o3FYf8gA2vmEa9ISCXyyByzFPiRlyAPrVYJ9ysbGWsQUCi3QRaafoE3x7y/d5a4WwACgZqZEZ3nGPP3nvwmMVm5rvhsf/QNuEZBu5QflEtX82j7oATlLtwHg7sIcm4pkl5viXItV5iHfH2x08m6Dqtlv5g5sba8yF/o7UhuDd54n2j/D0+lZww0mZYsv4OLOEZilWYm1xx7jao92pRMHMYAd6tiTUdgIPjvWACL6Kwlxzm+vGcAx5NPMS450YSj9eZO8rGblzTbu8NFQjwSQMcEpIBCVfJ2X6jmXDBA5xHBSgQIgYcAy5EOLTaKpvSb6BiZElhjbyrpOzbBz95/aXK8ktGW9f2du0Tnoqf4Vs15vfpwBDu06NlDwN+RjlV+AhcZlnB8FdYgny7qVV4KdZ7GH1Xy/QclskkBqKZ1Anof9FO4+AA/0IR2EUmMxv3aIHb9fjJSNFcMUJhzxWcPP8Aq5tV6OkNlhnEjwUoF2UXHJJbW//DGRaUZIhwkOwT1XA4ZmiQ31BvrU8BHXKmku+luLnZpQ8eIn//OKUIhA3T7HAXtzzyzawKR00RJ4WJgSHM8JBF3fL6Ic50So05IX+yIWTYgnxsbGMpWpMcvhl023PJZ/u3JTVPIZwdiTdO8wLQbyQECAfxBv1my8JIdDlLT3ZogKPHe8E/nQpH7q7HKtsdpLmGvaE/RCWULEDe7sumnGOSkF/EJnmFtpQ5tMgzPkNPDa7GWEU0k3gTXt+Mk6p9YF3smXFvIfq1GCYXtk8BjL7pNw0ikfHLM+Na5MXSyDXKQs+zP02vxfwispd4sjze3SIo+LWZib6Wu0buQ47TsKLaRiuI7zR719Qzf5W3CdbXcynVaEOphm0eDgVrdnQyXYf5qjo07y4SHP97wD1V7mIOMMLwu0cP7khTClQHhtuh8Y9BoXaO0NhiDBNuDJimm/NQ99uw2XmLRc29oZ6vKTLfkqs1mnRSw0rjPOhPcko0t1dLYXMs8QeSy0QIoz5Ea6lKwcg01QG/VwuriSTe7XK9rrmTzBPZZvuA4aG6o3zf+aW9IDNR72IDv+L0c/5UGBBdwt5dL7crdeSAHdWYmishuYsFiA68FAhw6KdoZubl7XPt/8gUbxamJUqSACxUNhBqd791DzNNvP2lGPczJSgAnI8+EVpJdUps2INMcTglOISkJA/xPbmuQSnl5ves1QKc8YLUvrL/xGtW+Sl7ET6h8Le7Mc5Iapa72iTZvyrwbzDYVTrW9HBIFfgZnjVad3XlOoAj7MKRhv4SjXQoVntKy6CPAnZA/icOrm9Q+GhW6qt/5ap03qSJRhRmHZG5ac+TaWbEM2+3UNxCgxZb9Fqgj/Jsrk1DD2DEwb5USEkZZH5Od0rKDUDq5m0SrTAXtz2D7m17MEllU+G9t9c7RsYSCgevJMiSnF46A17DUrd7IZ+PjpHcvocI66zE+1W6JLj0NMCa8z0ciDYfobBhf7STn6BSlW1TzsB6Vhq4u9LcMLP2TRfrqT5zmynnOsoIIT2CiZXrkPGQKASaqM2jOAf1V7gioP9GtZBN0a9UW4YaWTpSzQB0Y8ini+gYV2oNkKztyCA+caqlCHZG5l8Tf53IRp4XFHMZwRPKZEdge4ZJw24yvswoE1qCI+Sowk4Iu0ftDUT46NyUu+YvgeyyMSNY5LkbXIfMUFFWOtIgn0DxVQ/SarFbdK/eXmULdnQ2uWbI6ZqEXP1BSZp+xLnWPYHv8TGlrlIaK471vOIBgJ13JhjmBsE8kyuTrYL//Wyiz6MQh6sgT5xuo8vK1RopT2SK19zg3zRjQszlG8jf5IziYMD91QdZxaM2H7JaoT6kywwv9h9zl5Mtwn6+nWCaqWaoS3xX2AUvcOznltKZhgmavdEYhLfVa6bEGEVT9HnTv7aLRFh7DyQ4YIGFGcGMjj8z6wmEuTnfl4szq+eIhgYFDZMNHyj0j/ZGxapy4My01vCKl1+V79OtXB1F+BfTxcjgfG/e8bqplaqMOGOskdjF2GRExO8R3VlMg+si0cM58CBeMaO13tLf5qmVOAhaMd5AURYbYZx6SLf6u0cKaE2XC7SsI9wwExcuM84sK4e41dSUa9GibUMQBR3xacCd4k9+/3RbBnJAPuXcTIuEL18Rr06rNuk2nObMs/GFriCsnDvnDQPhE593kJwDxXA6xRvjbPPNj2tx3bC0sM3H2Dn5hw08AYwPaOVItC9SvSADU9oEWdpcEvtXZbeKg0OukuI1/dB9dpuBL+/r471g8re74rxMTYLKWEHOLJlU60WvEY7iAvbcsK1cy1VM8VCAn6SEuJXGwTyy39ZcUBxubQTqB/RA/OYaWP+w+bt2+whux9nGn2HvkSAhmhaJvcimPSLRM/xmdCvTsJQJhfsQGjdbGimxLoPyFA9kWco6la7Y9cprfHeZ1K+QPlBR89qTTkweECoEt9C6MuF41/TTyXSrIh+SGSvKQYhQ4Pe5E517qFX/HbIuPwuTvkPrRnsmBFYvM27KzREKtrax/Rb0TcIzla9zyzDc4vmICeAphIeEK/SauS5wqmvX2lmtF+qHzCBK9NRAW6UNrAiz2oYFgs91JwknxzDLNOxWeGcYavs1CGc0o48kS1vpJExNU0x/WJN9EBmDvFJ11F00+y94Rp4ws1O/kuC8gPZh2FcftClTbKsIo60B5eG/VgqqimecroFMzwgiXYJMY/3ml9dscF/c+bV841AwLyJDfyIyxU6wLCYLlI+c7nYaRRQQi+OqGUhGzhySrywulooyuvSrpWWmrzGfjJtF31blB5hDAS1Rs5a8891XKmUb6uvDfJNQF9ryLi84Rw/4BDocuOH+wCl0aSUkpr1ALLiskihEJzYoAdHfwFLUvZLP9kkki1sKgO9wUfb58wqcrlNOP8N+GI1Xy/QNg+wAIoa4FBn6rQZt0NER3mSHSwUGEwvGWuO5l4q5mPF8AXMRD9bPX5+ALU2DPRz4Yl2CaBI/cCJRCoaujivXLSCiUr4G5toU1BFZBznBftHtj20nawQQNEiCmyrKsGp6R5ob3FH+kilUC5ewkBul+HnvoqjU5kR4c1O/w7NknJOcJ83DTYouFkjldjOfwO4vLdKY61LdT9oTDKGuMK0R8QWP4J4fivSMMYBXGaKBHcIwB/wmOzM5NXlbX2YI5jVR7RfpC/yxWBrUOcqoARzjyNbItGV0zVHP/bjWTVKikF/Ft+gUJwKfA3xnbUAsaxhRzEEydd60+Uq6hb+IFSjp/vbYlk0ijKKjAXg0GJrNE9n3RCNNZbKrJQTj+QSrJRhFywnqwNkEhJF+pCuNrlErq+fbyv6GqfQ8kM2TEZPpVTiaDdPsUFM0SKFD/SIzlswQrxT7JN+unqXKR0QGCda4ucok/F6Cj7xo0RxzmfWZF8X2HeILCq6l3IESk44UR1mnR8A7xGzXuEc5uy8RvNJB1vphCKs5938OED8PieIP8hklimdgQcqzTZ+olg5w8UGthtSKFgCUjPO9NqvR3h7ddJ1xkEdJoPwsD/IJO3S7mF90+yfJlgoBUBH65WqZvDAIlTZVq2YGC4Q2AYmSPjeKNSgrWAN/IHEFmSFvjQwDS4ummxv54fwErOD/8tLh6LYYCS7yifBAQyz35cm1V3IYV3/FuPeJfk8HvkGAZ7qV+RgPMHotIRyaDlT7xC1AXdHgYlmgfUld4rjRcmJ44TIsEWN1HXFcZwg1np7K8b4jUuXognvpyzEsbZPOryrAXWKbEV6ykDQNEO0PqANsERHhTveka0Vmc+sHmaD8g97pWDG8IVI0qnDJebk2nk5A/M0Ikb5jaXNcg/MiqSbvrwsHjYJgkHyUc78g4tefwZ9kO5SruVoUuNbC5pogP57Osijp1Hn5PnPdQCtXaPXS8nkHausNRjxAcPLe1EStIVGHv0BPVLijPf05IX4jsfS44pxcXTJ66NFeDJvwb8Bv8W1ho7G71atq/wEZoCHzTdb3CyZ0U6hyT0YMAE0fH5ZohhVxz3WKaW4jOmoHmmhK4/5xKNZYJtSlHLAfK47jmMc01hmDMWjAEzcap9vAzLENT6w0qcS1UwhgPF+usYv88c/u+fIcUSk2mLbXdo/ATY/d0wkg85KoMOfuQGD377LtZKn1eQvogyr2xuGqwE6sn2IIiiXp+A8HK5Y+kK3zcZPqRhkdarfpZWRjP9S2D4DhQ+k1iuEMMilZWUCJNDdx7jYoG4p0qdjU2skdpDlXvFA9s0FzyDebWvhzO2aVFQii8O4w0YZ+YYkzbXCryVjWawTnEtnynq6cVt7+59jueAPu08j2uVUSoypDjVzr1u4goaFNYAJdgLYiuzbeRdmjnF0epavnBtL8Fmqqisc8D7B9vqmCbbUvoD12N3Sfhln636O6JCdHWfSVqCU0E540qKDtQL+c7RUJVWQAnaXp63p1jW1EuTo4gJ3lbSCvpNS3udd4aC/zyUDzIG+1p4lREzSOoYy2yoXrGDlxzlGQdltxjZ4uYSxvU2utOWO8g2r37dHRUNsl6X1op88CARPo0QEPEmNlDWFMdxhE6JjKoL8iE4SJo1rIyjfai3UoTtvxbBPbVsklBgI6p3qZPpX6R0eHShMg7KLB12+zLcSbBRgqe8JL5pcVi1MKikqlCGi2Dh/6Y5xDqDIdQjBDCIYOvhmFb2NRoI9HpDjGBtObxesQ/3BMPtrAXDQAFGhybI2d531tUWzta3bZ9UySDZD3V9wSLUzqp63xx2VpYcEv87NnT2BtZokzjU3J0Y/yYWSo802trPO4irM932gAX/P9oz7yEAOpxnv6b1FY5uc1ioGiPgNS1S3XWlE7F1spKkNNogG1CCLenGslrR/Tnm0PNiuk/QdZJPWULXG/i47j2WaWVKsxA19HFDabFm71+IXJiAtj/xJmcfqQHa5fcEt88c2Mi4IsYRlmywUUt04BjE4b5S8BIkBakkGoJwGGnoNMxbg1voxt5i/3R1K5Y+wO3SAK+rMfDRpiTvMLppvAshBpRRi4v2GeoqQTf5SmGmWEJpxg3eYJ1m0dbVY51NeRHsdZWsm3b85CTJ9L857wG0cohqY2XaIKqw0WbzESldjyopxTsZZt05slGuWZ639B7IJR9thTP0/NASkoN5ipL1S4hZ6hfpB3dvyFeq7J8pr0dLS4kcOaFkDVTMONVsq0O/u4MzyAYbWbc98ePWCZSuUq+exhjlO90k/EpeZNUp3+2+fOUFMxjoPgfcDRVt7ESEMukY3+jRUZRuezLgZKCPn3f03BjA8NNSigCUMcETFSWwWrv7hlX+ZWleowAi5WBCaMkVnDvjJ8jQxE+BfTxElj79xtQgkekq7ofCWKt/6DnlJj4Bvkaa24Rw1jQFKoYbJcQ9VTOxQ5AH8SuYnYU5wEtSCLUag+DPYrapMOb+owreL6dfoXNEB55DndymdcERER3IHCDSMAFEyAHzZptgs5WNP9IFIwXoQ9nVxT/p5A/94KkO83jNb7tRdk72HpKY0xu7W3QB+nRrpVl1IaRdshjhEtj2wmiuZidwxWSgt7Buz9wx6eWaQItd6i3UY1tT0TLqzKhC2xgyENB4do9OQx6eboE/xGCMuvl8gFkYTIl7l5eTZ7GTC8/7pybcJsMq2xIdFbNIkIn3FZ5eQ1a4CnOzZg5x3H2tTuw4ja2PEf8CNn3MY6eO+jiugmq1g6Ew8AW0cpVIXEfkKMvzpROgX0NimwsuwV5sKfA33m6pfrrN+XCbTGgeqAPF+s88tcUWytioOt4/u0GScWtdySHozekKqEh+T+FscOkLKVjnN89HklqJp7sAnXx/C993nf7BC6WPSIm8+HqfRd96rxgxFpNUjozxRbBwYBfZaUK/T1UArWaLNcgzhI+PE88fFTzBS665ySSqunq+hs1uuDORV4NhQkf4EoKY32r/Bj4v8lcrxCo1SvUDiDLNOszl+RPFFixeoBbn68cenI1gk4/uUPQqmUC+TDggpjrX3a59/xcXFNZkQYZaM3riFv9GlT7C0ulZm1VIDuBXnY/8I/XXK8n6iBHsZYF4oBQAJZRsk6H2N65TZU6/aWmySWEZiCDge6d4hbKpH9ooPmfaXqCdjSSpgUCYlr081VzYCvpNTn6cdpem2zKdBg447zoY5WNBNpVJhiHfLsHr/HePczJJmxLc58o+j+0uzKfyLt1WzRzUGQE4h2+l5Mw5n3BBaosWCe8WNVPVEsF0gljp7PBRqHduHt9wjOTLCd3CP+mA136+T8cC/BQmZcYZx/iCVb1teXWOPADEESBHygPpfN4n9IeRI84ZWnuWJbygj3XS1zzr+KEwzSeGJNkuIzuDf+vhlFv7GjUd3FJdkX1rP4B2mQXyAcrkwGSiQwFGlzbM2N8riZpehqTFH8QPuBzlDX52nHqikvY6o2BWdrYUGvMyP2LjE5gmhmyAqulstWxIG95tgYH2ArWPF/nSjlKoUqtC5SsKSO4J4PmEZP8RDCfTYRHcI0g3mjrqYsAE4MCDE/0tFl2NItzqnnbjzxfI/t1Mk2DRD+g1Jj2ga4iw5gunWHVaiRcy/3NBPeYx4VGSUJTm31aXQEopnxbN8oBz+oJR3M6+FfEAiHKMb3VC1jr00Y5jwVpsGvp3Vs4sAXDPHORGk1vvweND3j88YtJ6kOHec9z2b669/H6DXtQD1j4QN90V5abbGugoKFySFzykU0kxkVq3Cc4wh7W1A94OEDHMQaKbk37C2hrg35Q34TGMSq9DSlLtE56EpBKHHyc25UA41TsWaewOhT/eKejB8xTCOAdbqhzf5soTkoN9joL5R5dH9CnXYlhApjvWybp59x98f60mA+oxWAqQToI7+FKurZcnxQtLCOZvo6GLVIKnW6aUzBLvMdcujDo+dsc/xfe0du8zBRTrPT7kNTpC7QbGUot6q5yDA8Y0InuMCMj97SepgVuD6IID2FPXK9tsaFjCKtue4w6iOTEF+FJwtzMRSOo2uxzEBOvn8nmdYXsF12OjsoN39JZVqMGEJtU7qnuNQFhwz1KCw7pM6hYnJo4TMtMEKU//P+x8iEKPirgY4RAEdL8Q3rCfcKapary07EXlG5MyzB4tboxSjInzGuExAw71VWmHalsJh16SB8Ql9vXtX6RzVTzRU8jEzzXj7wTI1p8/wjiFJ/sOKR6mSsXPpmvLKgUt11lGiWVJHcc802afRqSKulGXGFkO8lO5qq172com/uaaQKl/yAz1Nw8HsFagtNAci0h2U5MeEO0pJFPTCdlnkCnFzo0IlUxoPPl7mpqQZLKJEZCk0mKYWL1Uh05vc9Uy6PGyVc4xLAf0RkqKX1Qr8xXFe9oe9tbwaoRLfTbZdpiu2gCUuGe4oJgJ3i6fX7h5XkXbEvHBlyGLdGdImwwp5GRWPeUi02OeRYGVoyrdCjpE8mO4h7FClKR3iZnpbYkDh32mRkwLn1mNqIlnxToMD+9ifeYELl/gNc1Vg0uds4EnunFwBNN7v5yjct3ZAMHeqCrUC5FovWtfeO0q8NWoeYtLdQHPXXbuFA4kiVKRL9I1goqLPdkJEzbLf52khmv12Bj1yJNInk7vKfYZEBKtdfftpRKXDTUaz2pujGJbJKVBylGwbdH43j3rGiBSkCa8v5Ne3M0W5fmBP8oUp3mHVyU9pDnU/Y5n4goCAsBzVr94ETuiVtxlshHt4t9vrWN+OtR7saOMU/TPM97vt2qXb4V8vwkNSvs9z/3cEIlWYHGCVHWwS2cfoADARJ5vo5S9D8o0IWi7P8H87ByfnQff0fJzsDm9QbFnaFjKLcztkHnPVFxqlx0/wkRmHb5Mvhm6SaaypzzkGDxAkjX2zd4qucgL5YzJcoFv/i/0Nj48g0WKy59p5XpLZMhVUrJleR+Zbb4+zQfAxfNQqSowQI0i4I2idKO8Q5Wj81qvUckh3zcdXuY75d+ldodXaWOYNAiRRHUsoGmiN/AO3e/0RrhvLAjlStLe9w2EjmWlufBOs0noSrRBZiScdP70qGDABCsDzkBlrFBiNp1+kRrgOcTq/ATCMHEm2HmXi4xe/O8N1dmnfdkPuFuiYBMbuFuDtdE7nF9pS4sADskUGX7/D+BejyXJ56civmdTBMFPrq6FcfjaQpqu8nOJc5Z/rGVqYccC3MWdfPdnem+BMx7dIg9wzST0F7dzmbn6aIZNeTLhTrSd6TOnoTjnxe9+uUz9DOsmMyiLR7Sw5g+gX0RokT8agA0/fqdwswP+JuLq3VSxZnwCtADYzbtI741ep7DuNNA9jHaLaGJ67hLf+ts1l2xaSaglOqFDUyKZRb0p/yeTvbUSj2JjF/lRlfvENJuxaair7myRTsQO22xaffw7y8K/UKZmdgHPYUqJdG4KpX71S4hp3vPwbKp6WmSZLsz15Qi0rm6ql9x7rVPsKssnLm3SOPvhtgKXekI26E1sgX9TLKlT2F+9YNb/2TPlEChatwHg2/cbmot3hIjuUK18z2ySUiE5pzvWyLtS1DwKCdtWc5pcNXftM74H7kS4o54A1xkAdJoQ3M6xbtnmGsr4iizRWLxFjTgsFKVZrZ/mJ75VY3KBV0yJWFUtqAnJQZhpvomWIOU2Jm/ZXaOUhFbb2UKaqo8O2VHVdoZUUWHWMdD2i3bGXV1qlyAC/zIQSuk1/1iMepWeiRLKNhZ0pgrJ2PcDttATl/+6YZJ87D3bGwNG+QHRkOUOqHJDN5kEPdsMEHbKOOtzgEqGg4sp0AgRYaAPzaeISp6Bcaev8lu6S8MG+E9qKcsL1ciyYZZGJSrRck6sTn8mqmOoPfoC0fvgUqh/e1K/Jr2xpF7t5wzx7bQv0iiOLNkuIyiQVtTeikLMU3xQkR9mqlY0YLpfsDDHNMbozGiuUBBXlDXL3tkLqrlagpr8JscRpmyVfUhAwSf/+Z1N6ikDIOBRX6ZhbEfGNt5gtRX5358a/ic5Z6InyMjhFaaCGsbvmSTeHvQd1Rs6GL5JobjgAYpQTWKJOz//AG0SnTjoCql9j6+NE/0ANX60G/Xfq3322jLt4YgZ4xaJb4hFVU7PBuX8qkP1Cgor0kBlpGdVLvYhrBzhMPTa7WSIX2sSpFKKn+gbku0+2MmXTqpb3CbuDRcHk3utiNwykHxKWfF8XcUnPk/gPsZGkEi3mYUmu0pJPfNbm/XKJYqOFtfYqCrUC5FovWtfeMwJ+f2AUaNjXSv1IQrnFgxV+jHjXYpq3c3MeoNTTWmUMNXsmXTYxwf+w4gN2w+2cI5sZX3CLKC6zHv+YVl2pwJ7mWcFesU/tCjJPtH45E6YU2weyX/l3PAuqbhQo7/HeYNQ4zrEBHBoihXo8oFGySEqJPZrTo1MJX/mOLgBwn+Dh7wMyQdHD+FSmJrqNbyeYufVpw3weZJrswcTLJ1xhLbhI7pYbkG2YF6FfhFp6FKSCdIjzPvCc7Z9ayLwdJqwoAmKokqSjK4v1V/bfY1fXGzHLdzGu3zNVlptkEVnoCwOT+s3uB/lLsHN31ShXWkTwUyMt6VR8I5NieGkHe46onOgbXU3iBXFhN80kkFwBKk0BeYfLUvnFMdyhF7t6PBMtT4nfcBvk/nWANbJCd/puRDxAIhLtV1vLLl5p+eddIdXS0S/IR3vCjtQ2wLSR5R0p9TNVcodCSDNT9XJ9w2qr0S1pu9lmEjvTZZiRUH5ZOftrmDAIQ4A/HJ+sl5SBpd0mwvzAN/xsFaQTwxLlTTw7ukriZpguLDWDNAbrFGoQDY+gWS8nPg0oWJ6WJhIRrtibzq1Ra4Q0XqWjsxJpH1JHNlTva2YbN/4YJG45H+Fb4VsikVKDatujJWxUMsYBQTwQm+idxxj2nOjK4perY2RAe8gFF+ZNsj6jkTQ1k2Sjqw9+gm4bItWQVrTGfrhtwGpVkZokSAF6m5cJ/w72GivfLi8ixKMW0UglhPV6uESn+Ix8uK8PdlT5R/LKzE5rUWOq4NvzRQiIYANPKRGLF3iP8cs+jL61JcssUBcKOpC2bKNZs7kfr+s2lifQ8lpvFRkQ6lvtazRZZVVWS3jfVbONixH6CP8QpVt2vziVLhoTCXYf5yL+hfA6irU6aIm8CSGQIhkRwe4fPPpwXThe0NSgyYlxykZZrxDyGKdaqeOkjbgDTdFmS/8w+8hoLFikZ36RIdU50O9bRoCgx/y55RX3zc/MfNgRbh8FVTNOeZfiGCcuoIy3hA7eJYx/O6fQJasUK6f7WmUaI92ohUBH64zxfffHYRDdWSIXl2GV2AYtxPTOOIT2+yuL+obC0KABJ+puVLc9CjwwOZnw0jMLNxrYVHIL87RrEX1bmJVqCcFwkFjJoV3txCzeZawpC+xTVMt/2qqkbxInOYl6YLHZ5RA0wLGBh43iF6Q0Yp/2R4vBKQ5PtgPMlSPR5QU4jjHwoEh2FpBMdl2tNb5N+D/ZbOv81qdY+tLtQIubewy7POJP8QUAArxeUWBVmc2uHG8KYtruLSsHtcANl2wF46Ch33OxS7+47plmBOuDMw7Nj2FGJuRuXfXEj0V7mB/s180YM8rxEC5Sv/RkHC2Xx5ZsRCLnJtN4fI07Nq6YLN4zyvSZRAYhWG5rMgEk1BuS4ssIt8DDnn5I60Txm2BhcZDmkN3Ku92mJi4TMX/Z4Wv2VymcpV8uHFQSO5ykYjTMap1aGmDMUGCV2YZwWOzGbl9sJCMHvAdK2C8E8PsmFLE6Cj3+91MrV/uF/BGZn2XXL/5r3zQLz8T6ndSrS0fNewrphbRCc3d5G27bEgpnwbd4sIx555Nr73NdZFS5R/HJD4ns0uApYFszhchIo0AcOsJYhOsdIxnsHiOoLwfggADd5422LWKVPvRFNW99nSzb+UM2Qs9GptehMO+b5lZUSTqaEPbKjB12BP6RK1K/e3uWJ9PDijVboy1nnOktXWbpe51o03wNswgAxSrUd/Fnim8JBwdy25PrUN0C6RByiHBNufO6EOVFy1xwnSziqZ4+egu3euKNMkZqkm3AnNr6nabgPNFyiIAAcNKb/ctRAGYbKwV0nmFlagYg01mLcNSnZ+/YLaUaIq2xHyBT7ZPjzktNIUY7920d+4qHGieSFeMXX8HuBDQUIx9zPvSW553YivJTdbn9zm6kmiwnKQl+nD0CPgQHCyTe5rZpHfbQEB0iR0/+HRWE7BCkDeUXrGhtT7oFDBOnA3N9sUxgP0+2LD1Z5QfhVSIS1Nk20aX1rRC5DoLGrYrU7JlSS+fb7xfqmCDhpo6wy40RKsExquESpyDUIbvtB21S8M6xCweXbdotpHrOINTMD/qOQXnNwYgrWStOP8ZyrGoGoFWcFS5KLO/jHbFxyyhvPUt0ASkBsI2ERSsVNrQuXbWEzxJiQcAziI/a7FKpQT+DeTK/hrcC0oN/l+ht7ARsqFhudCtd6xn0CzVF2Bo/RnB3bkOrm0OLOx7dYhMQSqrW5Ev6kygqOpvqHFFGdwmycncKIurM/PHm0S+as8m0Bw9H7kl/eTMLLdLVleiEA/CPVEu9lODPZ9bqYnKVbtKcTqOIbqS5jCmilCPuZ0M2ymYboliQ1jdF/S34SKTbFp1jAUguj0PSpBXlyfgPPjo0VjDFDBR53atkrJB4ppJlYT0Wr59yjDsDBZXw16VsOsFp2hec9xRIblbcAHbB/9ju3OatKgIlWxtGelB2reIXvHbF9bVnB7FGpAx5CYQN4xJk4zxMMoKaR7QYUqnVE4Lpn3zTe8SpbW2ANgIFjPONNfu3TDnzAzU6qEz5W7PCc0hAgq1X9zG5lDFGiJWhyJSvlBnGJ1/9HCSZdD5zzfhDDRG8kTe3PA6uqtYq6fcYoBT4BvlUCU9lgvm84BT2jIiLO47HvMzWiG7T5oj9F+j2ONThUtgK8VUmJq0a8jwDPbHtTvGOtkg2m56Tfwq3uyVVs9WYGGKXEOYSXkB23m5D9QlyP/gUJV0YivJTaOVhXX50T3lyfFwszi8Wal7c0PoAOH7hjCdBg46x0tp8XJQO5hqvhm6cJ+PmhHnGz9GlCTn3K9b1KVmhO2ocYJs8yKJSlJa5R3Wl7dC5D0MDawxQaF2HXv9Dt1jllyvqrYU7RgBcYUqxqmGJ/LtEsTYjCXiHoYh3x0raP0j/fiCQbVlZWiTES3pBzZd0BnIXYppusHYarxrTWmEHYaKoVvo7wT65q8h3AipC6BUc3HJVNjSjULiLQIMwkxto09SBpdznCbcL8LsyCzqZCViljfJ39h528gJ0eeGXJtT5Af+FmBogme/mf0xpWZqT59MQtodEG/tHcxyiSPPx4UAxx5fBsNSvLyWYrSSCouh11etU7hRjURlYccw6vPbO6BPUlOhEz7zJjJN8BbGXf8rmLigOtRfZD+CLbaY7DKni0uUiKw9/g28eZ4oCRKHTK/ovgigX25CkQMm2RooAtoN3W2+YKSvmQDdChB1w1mCvaxf+JpJv67eB+Mwhny4WUND1yvlwJt31TMFc9JfbvYUBHXwJNw/6CCVu4kvskdbL+RMosn2N5+1ZqeS21meQsgi9yUUM6Jlv7/CA/ExUib4akGGf2UggEvCfIFn0MTFWYBQTmeaE/Hm0j+1mVm3iMN6rEL8OuIAIxinY+/1iD6rSnJzqA0C7RMxTvELgBT0A8jhxyH3KBJgkCbh2PQ6u7oj0OaAPvYlvFulcQsTkg3wsMMQknpIRoQZPNUSezKrX74HwGWZibEB3BI5eZcOwsDzLI+qVoa64jnEOJNqsgcTJpcK8sDoKbB2QDTEEj/lNB1lvxfXX4Z3hrGuHNkKH1alId/05BuVvXyklL4/3lfTCfkFCzuYcoPDvn3TSFxrvCACwUFjH7tntxD6CuXl8HuHe0805mysl+Zcgukvq6H9Jv8VjT+BeRlVwyCsq99wilsqGOJ1ZbgjCCioX7FQuXyhipkbjURSE+Fsp5i0Y7aOTJuk9X6ADIRjhjpKUO0zzvCpBrZlV1mCBwfOAjJM1HKRGes/3P3IepFiOniSIf/ExjqSk1ikhv8j2y2nYINjFRWEYZyXzzrJChhonw806ggkBqdlpE6fIsTSmniDa30C6233lLlTnIQMgvvVeIVuxgLBJy4NpFuQovIipj8kKZMMf/d+GGzVBfFEjVTow+BVq0JjPYkb+4PpU4b6FJCE/kOFeJ1hgUBXbolDruueaZ9xGhnpRX+aWEoIhCP3ap99jr2VCN4QIn7DTaunqlPe7SzZu+ZBgVXNLNEGDxexfbK28w+Ed3Rnrn9wsU1/KrhLmz7tB+j4vD/FMSMdoFCMnLhpyMRfxNCMVZZL8BjjU3101kGNsvM6u2teKvtLMapoC1/CC/V/h1zhzc51tDg7bJoKkaSsUPbKGvTBhzb1boY0wBQEJ7skzvTHb9FaaF2gNhnWEGlAilmxTL1kiZ++B/kQM2maC+iQ+kDJ5Tvmn7Z8ol31NsB9fl/KKNHs33eWUm1fjg4i5TAFNOZVuSmJSbbHwEqyZXw41Ve/t8g6jIwEy6qbOuollkmVRVdIo02i/p1b1F8pTbMzCt4MM1CXaL4F4RL038JhvmQtBrhBmqWUaeT7cYOc3xfjN4poklQtOo1Sl4L3A+0hFj/VWXP0JRJm4R/BPtZrgK21EtwEHmOXJOyM8ByZvWW+o5AM8y+QdYRuaDmPTJWH4hS4QSFdqyYI1w8EN5lMpVeiXbeHng6DAlN/xlSonOI7i+01w9TlIZJF4B/jDSEl1EHYmPtQ8RNwX5ICHtwmOh2CX8Q6iCiesqouoyJzX5Jhm6qtd9zYHev8zQm6bcg3yyUJDfxp8OC3Z/EwWl2RRjzXLldo5QfSYZc/mOerD/B6RTPvYI+/rFDh6RPg0IEklwK8QKdMNGeMZrWB9h2beEk2+Csq7woZW/06zFS3U4+u5naMURJkskemvrQOxuoz69GkdsU4r0i5b0VOzQXn470Kv1dHI5cWKvIyU2K3G/N4pGS1p+RutkIISaUqodepHMKpPr6f3QHRKqoDpnF4K9RZk5r6H+4/CX7TUlCVYwpt4BrkbL58m5WUK/UhKn6Pe7+LvGm+vGOlqYwq2gKiSKgfCRq9ZebWikm6VGhA7mNezAknc/Ik9ke1f7ab2XKXSUsy13Hr4pJywLBZtdqrE/MnhlqnRk14yiDB3+EMt1xjFelbWapxXBa2Qslwh1yooaI+1QZBBOVku4LvPezHKdLksij9Pd4A1wsLUfME04vtQsIkHC7UdUivbnpGyRadBq5zuZW9W8E2HG6Dda6wkH6pr1GpsZEv2hKTZs1xSmGLR6rrv2+UbVQq52JytWcKVfw7+0CjU+DtrDb0flh4pF+a79ARxfwuwPWTLYV4wAPrBjcnnwL06Jd/8DsmCPZCabtrckrPcY4Ss0SCtaI6+hskA/YGzdzwXNr+JsKg/i/xIMM3/A4YXsAH2JzVaMU/LTLDRmqmZwp+p1SAapdBvsqNMKlieATTfu/NwG3t/WGmkNBC5S6FRqdRSwiCGYmD5g6HXGId9H1FtlU8HZ549VPxJMDI1SnuHFsn20iIqqt9rYJv79WRTZZF5DjhIgIer2jn/KARpnd8YoshMahEbTe7bPpGsHiyxYQ9xAoUKuhl/crLfPnKU4iRsi/tJdV/zyBaevps5O+3Ef51Emy6NjXbNyJG7TnRdK0Q3PjwVsgEGX++Rb2mlTzrxTjp9ZBLvGraYb9rTgi5cL2G4jC2dUpAsAY29gM1V49J3zroHujM2mWNfTZPjj2juMkbkKM73tGbBOJu+RrKDX9B62unutg+iRMDHMp+ba17Ek+XYbYylj359MRvjQMGR7cHzf70ApKKE+OP2ViFVrBvzwUjBZJfquCzYvMPEhbcel2/WXIuj2efCsx1noq5OM0hYBrpZf3QvU6Y+j3h65w1nHfNHudXLBCUY7CHuW36ZAkt5U1n+Q4bRMdvoSffec3G9EyXaXRUpzP4x8A5mOAA5cmtcJd2xQX+HCoJ7GyNsPAXvXh7d6IMC+wZMkrRMLo96TjboKMH5jglXehD3eDtD9urKquK4EWhVbRnoHVUaPIkz9Wpd8YYGDbYDR7xIlIToXOPFuAXvZPQZIIKG0/5XKa6uVvmmn2Kndt3k37NZZV9fT2+ZrOD2QylPw8QxhYQ2RQCZPodiyrRK+Ln4mD4B1sJ5G+hlIogvZJv7dewYbJ4zAnBBRVR7BfKybp3zU9STqErUrpmcjaZYK4Pr0qLouEd3zUXP/oB3O7rIPH2GvmR5UmCds4cuWxjXrwn5duGdY9RZEWyEhLdAyx39DP+e415vcn9aJR+fkT1Ua2WmWi8h3+f67ILy0L6BvU5CD6jTbe00SaVFxgawUNLjmtiFJ5o4ELlJuff70vPMTVdnijYs7Z/y7pYpciVFMAjk3S8DD191zDa7a5g5ws8HMsXMvEvPWHrSthsmU6OoIgR7BQdX581yOPsFsDGXd/+g1yGSPZVk095MKxWwvyLecxQeUi6EhrEMUUS1QfXY5k/9IS+C/MaC37VVKyQg1r83TPphfJqvU32V4JrEA+sQYK4/kzkOlUj+iYE10h+WOQ7xy3vCc+5/FvbNzJLiwzo5tp1ycEn4Y7kVotRul2FaGNRyyv6/a1H6Ds2KNZzcp1vezmmGJQQ1QzI46YB/ARYfKAywvTec97kHefXhh6+cZYw9xwOGeE81vWBKo4WH220aVqhbR1G1AboT4Yn4cfmRr1Pfy/CNsar3R+phxyYi9ke3QyfSp54EVLtcKyWwx6YAz8u8FF8jGJtPeIm22Ggecvr72zyOTBpqyPb7Zhs6scr0MquC+0ihi/OAioX9CjS14Je2BgaNudVLtMECF/VML0t0hLCw/NIyB1BNcF4mIH1Kr6ARLKrwGKkfMQj6F1oWOBkqLbBEZx4GhrlQjimdmQg5wL/XIFX5pOQE/AxdjTgb5f0xRGdnXaLsc9T7TmtFtMGFSWDZLOKyj3VSSo0zW1Nrn10PvldqCvyC+La4nyeayB+ijHu/sIPu71xiaDiX6slnz71REcCq0GN1esVhXtUJowrGOI1P2XKFsZMhljy6t145j4Ifrcm1cvIFZf1Fs7ghSSAW7kG8hIXI5tu4MKQZvEcITblSmG6TCZbxDvBWPgNu6+HGoRwQiviCtajn3SkhWOatcFfin/rEuUKfF6/dauPq075Egod41ItxgooVfEy+xDJMoeCn3S1WWgByFyUpZR5raVNkobvassmkEjiMRsprjTB/Lpm0z4CCfssUqBZTgXYIMtVhGGThpAstUddIdEi5fnJBoinTIGSsBraW7EU0gIxCbN7tpftRt8sJyjbU0yse3At9SXsWLtzs6SvM/p5eB7XcffKvXKiqkyCnPc0jk32PtkJe0moSIC17SakZFdL5C88r2kDJoZGtzfxJ+f863fvODpDjnizrME/mJR7v773WYtY3gr2JxQml2uT0bdJ5GJzAfAnINMpQBy5X6spz3LE9dVtjnp9C6Qj5P3SJKq6Wd+v2GeUT6RzoxI1EZZ4gca5X/ghEB/uPTP9cUQ/lUauK8I6yKHgVLNjcRjxA/6dmjrnxi+ox5o8+hOpfZ1VbWSAY5Wq0WDwPSssnwwR0y4NV/AIxUO9Hu77uQzia10a10Wt3K9u390/4uiNN99J0RbVMxgFtFKKtOsEl05tWPUjP+cSL0nTJcl+iH3JvftftndFf9BLmJGad6vTOvny2XigWskwzBMjefAR3pzoJLZVXSLqS0WJWEY5pF2tLN4ZrYm7LsQ0HXytLf739Vvr0zLkicoTtXaXRp9tRQemUJ/UilvgBDgIwBUv9io9StYg2E68bYGZggj3fmQWxTf86JpA4fwD2MKpAv1zxCTUGDN77yjk+aRi2T4zItZFQtkKZR3eNuJ+vxTYooUgzCZgFd1JjqKgSuPucPPKlzPQXdwWyH0GAJpdv/ujXvYrMhrUAx37HQd12B/vbJcqmu3Edp9NDmy6L6m5qmPS8DbSw50y7Wz8HPQCCjy6e4KXyCOXaVZ+k0Y/oldELZQ8ribMHdbhxWyADi0EzUePm7Qcod9ArrPVDM4yoX29YmVRyweX1qsdtlZBZc0CLdAiPEDyVrsq0BHQ2/tjhVxoKZwp+s68b87qc/7HsGyyaJFMj3lNDa1Hl6jUJLZeQEqRHHq6OjEQq1+xJ9UJubmFBP4hE3rKZ4q1g1r3/W6d991bgXrQGN01HxmFG/Gt1wC6fl5M7T9Ormx0TJB1hQDqENHhwEerJz5hqQmVtqVx5pZLiLT+J/8Ful6acQIGgh7D8bV08RMYZsYXOcsOYhiTcJswi1OMn78AwysScLY7x97oApXpBufKmhTOGK1pnktgIKY98cugU+dlRXmiAj73cmpK7USyKdgG6t72EpZ3fBmsC+fat33x+hXA/aF8gXfNFOIFd0TxJ9vtq3X8HwZvogIG/X9hENMAiDPUDsLLgjikbXxUmBSN+PMjtNI7/OqUMNEcuRjOZGV9ml+tlLda+gQHI89iaZp/cQavRoY6/gn8+MB64R0GPNZvhJyUW/DVCNe8/l+lU65TqXheY4h9sICiEqVFSHSYOBL1BWZCnUK3P5pbkJ6mAtoHEzaZE8//zR2S6nCTjM5nhHibWpl3DUnAOsr2jkPzCDxVlz4mxRotVPVctCiAQrempC21W0IS8GagnZJvpJgD74DkT6Qt0GubZF973SPi0uw4tlJBRJ0QMcIEbSS0UNgh+QzH19JFr1BAesxjna+gfPrYQJKw5kvvD4dai2h/Su0T2eeUQ9BIf0O1fnybRCwIgmeaB68S2tfVYOQsDnS8F8rBv2Pt4SLQ4asTsGzdGuoNdj6vMN/5vXjTPgou0kZYu2Z8KKxKnRzODtHE0GmxQAN12nLtmLMYqNhFyeqMJ4YL4Dv+ESUQoEKDyO4QnHkRY6gcGeZ5VQWFe4AbxD/O/eIA1Tl9CcxBraGuZ+SVCsjLuRTsAKZkjCY+G5ljsq3zPY1jd3ijNzjhYAhOyBvEPd8q6c77Qd8WUiSZIMy90Ayfr1SVl7QfwCmYQZp2e2P1APe1/g67I1JcowMY4BYILqBExXuSaKTezkime18Gx26e8fArg5l3goitD/x360qyQDEDm2W395dxixsOP9B5eKQ/VzfrE+ZCpkP08qw++AsfOvMC3uLzPLq9UKae2WSkXPYe4khvbugOzMWTe5dQYGSUJznyLgJguHj3TuwG7v3depESGWCnKrbVq2Tu0jy5svUlg27zL5IjCCO8ZOfjpUnTAxAV4HBys0EpbbZ1jSn8KOr55w2XQGZBgCrS++899vU92MK4PMc33RnFeGpr7DC+i88Hh0h1XJUnC9MSeF6BQc1llnPdqKMjygQcP/him7K5aOX8P72/4HG6d9d2sXFUZ+YP8MaaePRoXl+gDS3lYU04h1GtT4ZOmJm8PNcUNhG6G/Xgl0PQ92uUrNUO0TGHJPkLMAzvNvu72Ri3UnJHuB0Q9gEzGJo/ySn+CNrM33iQaSJgsTbd79EnrbZssaPZRZNOt0mIT2VFwSHz96kcqC4fa9hRIN4kPBe1Q7kBpQ68qaoK4TwfZJZim4yGU4OzT7ePqzSSTPEVzmBLTtgZzo/JCa9HLi3jQFizKEYWqwyeJeQD1NSKA80nBX2VHP/o/Sv74ji9kPNanlXXIf0XMhKkbbHzhDSmIAAP4C9NnUBOKJk7wUqKa722pjv9KgBz2EG6lOMSs40M6ue3GsUf5jLMf0tz9zqxtMMmoU14Z484MqtMUyuSSLQE0wO3v7kixTUDfslbq8jNGpGgR6GM+STGNo5SkmNwKr10iZPIK4d2HgvCcWykXjdm/QrmH84k48/MTZJrUQO1MeiZsULk/xj775UK9379J94IMy+PdIG/lmrdNyBTv21zu3lmAaRh6Qz6J+7YnTfMOzsd7liW+MYX2Psl4NWAW51e3g/SEjwEhnDztZJO7A0+E/1LNbRweji7QJUJ0Hqzv6Ew7y4rYKA2+eLCHpW7RJWG/CX3es9wmHoTSdML2eSAXa1HLznSYGDhGStR4BPpYb9K/v/LWblQGluaEN/wgXWjnH+pkLMa7ReDVvEtWn/vJs75j1roCTEk/SgUxB5xKZRu5A78Gtfa+gLgLSgWoxP/ycMRgZkA8OexMPgrzROzU3VT9Dn2wJNw4h5zdK4OKds9FlPyIO96oB32wfFavVFLMcJs9cihUvHPCISL/FH4LZdElycBX9sWxfKrYuV4FSn+Vii2UWg3iiLsf4chlZ68Bd4nOhqoPMHIzxu6tVm8rpZLsFG1a5AhETLKSsThoXTaHykmzWNkh3BbeONHx0DnJcbn+XuNU3gcqQiVqKhKyfd2p4bsULQ11Qb3IhM0rmidh6R52EFBSadyFPYTBEXFF+tBt0D22II53xMCI5I33cHCCbe0U6S7+1fzHq18jHBiIrxksYTeLYcdLjGQPDrVGA42qE/PbpFvppaUMK5RRBD9c7CzuhCFqFWlnLYZyhSUUZFVRQa7WLKxygeHFgshlhxkjGpoLI92uAWldtjx5U+NdFZ+tk2+jIkp+Ylgg6LWet00ogOmVVpn00mLqPUg2wUMLfxbW5BOYRyaTc1IiEmNh7MM7AYkHq9O3aXeC4LkAfDDkhD5cPIg1X9fZ+Yc8+y0YfYdIDTlI0bOR3s9gULNMNky1q3lc+RwcxurLMCirFn4nkGAtMNvkH6HcaJQcFbKVb26wiiJQlQl9FRbo31xTZRAqx7cedPg9mGsWk892mmE6s44kK1Djr/qU6Ve/xXpDXhB1g/ipf4Q/DYPPv5QYZ5QYj6Tb5Ih4zzpkshenFVEDPxWnJapVYe3JaGW9121Q9cg1zAYDKx7+PyHLLlXT32vGD7ZFS1prkm7BuwuxsLaIsw8F2WrJ+j68FzbplqFtZQW1Sm/fdxgYCmqNdvM7wyCUmB/hDQQw0BCFNcy0kSmcIDy4X2QX1kN/Vmkm5VH9/09/Zf+J/ESiDPtD3VPrE2yks8jgl4wBd8KC45RUiOdWpVy1xDw5fABlA08fJ4+xMzfF5noE/Tkx36hOsQp5kFQdIpLlcSOMNFFcGSvfkGMdQwzvlyJOsxkw7zwcvIDMWKjBuX66EXt5Rft5Md5gnbMDtU/FSnYDI3crk73Dy8g6V858RcFNPBDqS6Tb4/vpFXHHxZWqCLa0rtB9/d/5567YN9RsBWoRHRk0R/3pIUv3FsxWfgtVdABN0vRKNIgmWSKq78rpHpiGvIRlIKJRenraf2QsHbQWr0C5AgBEqRcgp38CIoDcAKsMFnISCVY2R+Gb89zxrXkY4IZGX+UM/TH1mai21/eqthcoXHZJvleJnWbCcXXokL7Az0y619dzwMVJOAsyDiKNJOjtwjDFgRdtRnT5tQjtax0pYrqa51B4R/4X0YblRiB3u0bvXhGbpc7HtsMOF/YO9Jyh2GXvKocwVhwTZR1/ojsB5OqQZGvyEG8YOAU4wokNJNPmqDFJIALCmClYwiOGCJY1CDUdIFgsIaSBt0PF2SFMbq70RTSuT+pl+Nvn2TGJvUEIyHQJLOdrgjnbEVwjQogyxIsS9A40nmMVbGajznbFBRgkSPvx6NgqLw0otXkf51B8APQHBoivGevud0ojlUtMIQ9Vt5GP03MOeV6mG+Zjos99WxEeaBByrzYOa+DXZ2n9mqeQLB7xR19LtFcgpbjBodedHOZHDD2IVgQ1BiDc89/n6+/BNhBaVSNbOeR9QietnSTptRf7A7wPY0qRBelfqST9hy6dG9bpjENhWodU5kqv0+mVbyMmD3dFQp0gjXyx8ItpotPkr6PPIFllSeZPg4H9gKVu4guwUpyR6psfvgRaFmdLvlEvVu/iZYg/CIjQuR8+f6aIOiDWoC0zlW3Z9g6zThYco1/5reKLIFHdEGqKzH6Jxhu61i6RIk5nvCjA8kbHGSMJu3W4Bm+llWFu8UPxVDfbd10FBCze+LK9y7PRDJWvTIY3QV8NPA8p1frW7qRiHmNGjQHoU7F9Nwt6/l/lu/eGqlpyTbJKSYygkSJn+pM1FFWMohAK+o9CVbbIflc7ieOkcIzsCk+XbgU3/zfDISsc7Oa4H7NL9EcrAtlNpddjYzyIYdNfk6kJR+XeA9BizitXahduYmXMOx1XWC5WNOlwSqrgUKAvulgmEXyD79hDyPSX8iZ7A2pYVVyh0FT1TxFdLAD3n6PcpWuugKPbzB82ju+xvMHgqJ8ppjvYoFbq2DeBmY1ykeYmekCo3pJY5heTMojWmuvHM1rlGmYv7sEyVB4RZx99oDkGYmhea+d+DL4beJQ4EkpNopGnIrZOZRYcRXWHgqCFGNS3ir/T75CgqGmFNFIYF2EZe6Y/BeXv2W0gvBfumbTYagBHk28P6an0yGLUG5KtyRPviYgEdtm/Uq0T4aqtEWxJgg7nXL50PMMibV4opjnLedy/U//VjYilliWgv0Ytzw9V5JUP7kvAH3wBv5eq0q62vAP/WQ1CK4Z0/zeKb+GDuGW2BKhNMQ52TMXEqBjqPmzG4UOdhymLArJDidR7w7HdMYPprnqG5gBF2uOA9rw123St0DWr5BarnrJF+ABLB69YrjpowuVHmYMtjYa3AowTeAUxH2Cf5n50yzeRxYrjTf9yeoAlqpjuY3dULNrzjraPhRHz0yq+8hggURxRakjBewhGWv1DcZEuEusgZwopUUaVvARlOzPIaSfV8HB/kv4Y50v2DoZGqZ9lZLtDLthUmeNDBXLFiZX2jynLpJd+prHNvwgMlG6DffU4BmPqXOqlNNPt2XVIMVieyaoJbzj0DCWU2tMuhsg7ywSaNYh/F7sJYyTwDGyKytfqxHs0/gJgOsagoS1f8JZ+Ab9Hyg1lhv7pOhOrypSeo0APfYhFWrtGcc3/EKa+qlW2wsba50K1+LqHZ32B5+ZqGLfRPgH/A0uKZNIkKLBIJBMNCmdJE/HXyZS1Cz5XqpdsJGTYpYBLxy6Vd73xTO+mGK+huBnomPQLZ1DLQHwfeq72DOUU2xc5lk8y10kG9Ei7m+LeoqsshPMVX1AmXjzheEbipBIk6zRXLsgqWLKbVYWkhLvyYpJ0zA8KoY2UJhlbCqWa5sY3Azu/sY3tC1jT6wlrs6qD9b4B8HftA+naPsllTxcEKRFlt29dYRYRjPMEAjhGzZHlmnjf71HtZrZTY5WaDLmULa9vXf+8SPO0vU/lA+FV5BBeW7LPsvqrnrDUm9mtiEf/Godc+BL0D+SQaa8n3yBSHIUw0iSmZEr49cgz66fHuti4DrhAiMLinGahc0IhGoAB9QSd4BvDj+eRpgT2x/eytFDrUJ9D/N899aqELyCeYb/lwKxNdcT8RAxKMkgw+LBcdc1KyPrQSO6WmVAwmfuC6JlgYStHdQXVS+SZoWtqnOmnXSSmuVqoWj7M5EtHyjDIu624C3dNgUphAoB5iIpasU373KsTIjh9Ha9T1YSpFCyvbBk2Klnq5rlecMwiFmKPQ0VpFiHndZk5nwRbs9uH94QLnDRJtFqgiTl5dlyjWZNOvV/mKihEsbeTcj53k/pcpoohzo8GbJymL/sH45tFX/FW1GQHQ8pqhA=","st":1701900044,"sr":1760113243,"cr":838392674,"og":1},"version":"beta"},"old_token":None,"error":None,"performance":{"interrogation":4197}}
    url = 'https://www.vons.com/ueene-suffe-and-swort-it-know-tenda-Enter-I-dist?d=www.vons.com'
    headers = {
        'upgrade-insecure-requests': '1',
        'sec-ch-ua': user_agent,
        'accept': 'application/json; charset=utf-8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
        'content-type': 'text/plain; charset=utf-8',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.vons.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    get_token_response = session.post(url, json=payload, headers=headers)
    return_payload = json.loads(get_token_response.text)
    token, renew = return_payload['token'], return_payload['renewInSec']
    expires = renew + int(time.time())
    session.cookies.set(name='reese84', value=token, expires=expires)
    return session, get_token_response

 # You will need to watch your own browser to grab this info once.  The hash probably uses a salt value in some of their javascript. I havent found this yet, so I havent found a way to automate it out of a hash of your email.

def post_username(username, session):
    # This should be self explantory
    payload = {
    "context": {
        "deviceToken": "8910a6272e41b85fb9c76add15ec89a1"
    },
    "userId": username
    }
    url = 'https://www.vons.com/abs/pub/cnc/csmsservice/api/csms/authn'
    session.headers = {
        'x-aci-user-hash': '425bb68859e7210a501ee243e9bc46705a30e366bfb3356559f743a551d8fcf1',
        'x-swy-correlation-id': '079627d8-7720-4c63-aa2f-cae3d7290da2',
        'x-swy-date': 'Wed, 06 Dec 2023 22:03:34 GMT',
        'x-swy-client-id': 'web-portal',
        'x-swy-banner': 'vons',
        'upgrade-insecure-requests': '1',
        'ocp-apim-subscription-key': '9e38e3f1d32a4279a49a264e0831ea46',
        'sec-ch-ua': user_agent,
        'accept': 'application/vnd.safeway.v1+json',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
        'content-type': 'application/vnd.safeway.v1+json',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.vons.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    post_user_response = session.post(url, json=payload)
    return_payload = json.loads(post_user_response.text)
    state_token, okta_id = return_payload['stateToken'], return_payload['oktaId']
    return session, post_user_response, state_token, okta_id

# I dont know if the date header just validates the correlation id, or what exactly.  This may need to change for you, and may also need to rotate at some point.  But it does continue to work for me.
# I'll sort that out through automation in the future.

def post_password(password, state_token, okta_id, session):
    # This should also be self explanatory
    payload = {
    "passCode": password,
    "stateToken": state_token
    }
    url = f'https://www.vons.com/abs/pub/cnc/csmsservice/api/csms/authn/factors/password/okta/{okta_id}/verify'
    session.headers = {
        'x-swy-correlation-id': '0f1745d4-f933-439b-bdb8-145f59945c7f',
        'x-swy-date': 'Wed, 06 Dec 2023 23:17:55 GMT',
        'x-swy-client-id': 'web-portal',
        'x-swy-banner': 'vons',
        'upgrade-insecure-requests': '1',
        'ocp-apim-subscription-key': '9e38e3f1d32a4279a49a264e0831ea46',
        'sec-ch-ua': user_agent,
        'accept': 'application/vnd.safeway.v1+json',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
        'content-type': 'application/vnd.safeway.v1+json',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'empty',
        'origin': 'https://www.vons.com',
        'referer': 'https://www.vons.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    post_password_response = session.post(url, json=payload)
    return_payload = json.loads(post_password_response.text)
    okta_session, okta_id = return_payload['sessionToken'], return_payload['oktaId']
    return session, post_password_response, okta_session, okta_id


def post_okta_auth(okta_session, session):
    # The previous step provides info that you in turn make another call to okta to complete the sso.  And of course you get yet another cookie.
    url = f'https://albertsons.okta.com/oauth2/ausp6soxrIyPrm8rS2p6/v1/authorize?client_id=0oap6ku01XJqIRdl42p6&redirect_uri=https://www.vons.com/bin/safeway/unified/sso/authorize&response_type=code&response_mode=query&state=damp-education-orono-dry&nonce=ovJgrUobDYQKhiownVT9jU1GvtkRdpC4Eoyal2SfgGu6ezXG5b03393l08xbDGw8&scope=openid%20profile%20email%20offline_access%20used_credentials&sessionToken={okta_session}'
    session.headers = {
        'upgrade-insecure-requests': '1',
        'sec-ch-ua': user_agent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.vons.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    post_okta_response = session.get(url, True)
    return session, post_okta_response

def final_refresh(session):
    # Refreshes happen allot. These cookies expire fast.  In standard tradition, I'm calling an immediate refresh once I've completed all the logon steps.
    # For future travelers, you would just call this step continuously to keep your cookies fresh.
    url = 'https://albertsons.okta.com/api/v1/sessions/me/lifecycle/refresh'
    headers = {
        'content-length': '0',
        'sec-ch-ua': user_agent,
        'accept': '*/*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
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
    final_refresh_response = session.post(url=url, headers=headers)
    return session, final_refresh_response



def run_logon(username, password):
    phase_one_session, phase_one_response, cookie_visid_incap, cookie_nlbi, cookie_incap_ses = phase_one()
    phase_two_session, phase_two_response = phase_two(phase_one_session)
    phase_three_session, phase_three_response = phase_three(phase_two_session, phase_one_response)
    phase_four_session, phase_four_response = phase_four(phase_three_session)
    # Added search for Okta none in phase five.
    phase_five_session, phase_five_response, okta_nonce, okta_key, script_Tegridy, state_token, okta_date = phase_five(phase_four_session)
    phase_six_session, phase_six_response = phase_six(phase_five_session)
    get_token_session, get_token_response = get_token(phase_six_session)
    post_user_session, post_user_response, state_token, okta_id = post_username(username, get_token_session)
    post_password_session, post_password_response, okta_session, okta_id = post_password(password, state_token, okta_id, post_user_session)
    post_okta_session, post_okta_response = post_okta_auth(okta_session, post_password_session)
    final_refresh_session, final_refresh_response = final_refresh(post_okta_session)
    return final_refresh_session, final_refresh_response

#final_refresh_session, final_refresh_response = run_logon(username, password)