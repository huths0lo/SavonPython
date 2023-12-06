#from oktaloginwrapper import OktaLoginWrapper as OLW
import getpass
from datetime import datetime
from email.utils import parsedate_to_datetime
import requests
username, password = None, None


class CookieManager():
    def __init__(self, new_session=False):
        self.cookie_string = None
        self.initial_headers = None
        self.expires_datetime = None
        self.x_info = None
        self.headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive', 'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"', 'sec-ch-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8', 'Sec-GPC': '1', 'host': 'www.vons.com', 'ocp-apim-subscription-key': '7bad9afbb87043b28519c4443106db06'}
        if self.cookie_string is None:
            self.cookie_string, self.initial_headers, self.expires_datetime = self.get_initial_cookies(self.headers)
            self.headers['Cookie'] = self.cookie_string
            self.headers['X-Iinfo'] = self.initial_headers.get('X-Iinfo')
            self.x_info = self.initial_headers.get('X-Iinfo')
            self.headers['X-Iinfo'] = self.x_info
        elif self.expires_datetime < datetime.now() or new_session:
            self.cookie_string, self.headers, self.expires_datetime = self.get_initial_cookies(self.headers)
            self.headers['Cookie'] = self.cookie_string
            self.x_info = self.initial_headers.get('X-Iinfo')
            self.headers['X-Iinfo'] = self.x_info
    def get_initial_cookies(self, headers):
        response = requests.get(url='https://www.vons.com', headers=headers)
        cookies = response.cookies.get_dict()
        cookie_string = self.format_cookie(cookies)
        headers = dict(response.headers)
        expires_value = headers.get('Set-Cookie', '').split('expires=')[-1].split(';')[0]
        expires_datetime = parsedate_to_datetime(expires_value)
        return cookie_string, headers, expires_datetime
    def format_cookie(self, cookies):
        cookie_string = ''
        cookie_items = [*cookies]
        cookie_items.sort()
        for item in [*cookie_items]:
            cookie = cookies[item]
            if len(cookie_string) != 0:
                cookie_string += '; '
            cookie_string += f'{item}={cookie}'
        return cookie_string




def next_step(headers):
    url = 'https://www.vons.com/ueene-suffe-and-swort-it-know-tenda-Enter-I-dist'
    response = requests.get(url=url, headers=headers)
    return response

def next_step(headers):
    url = 'https://www.vons.com/etc.clientlibs/wcax-commons/clientlibs/clientlib-jquery.min.1f2d1b7c8142fad2b09a92d1f906596e.js'
    response = requests.get(url=url, headers=headers)
    return response



def initiate_session():
    global username, password
    if username is None:
        username = input('Enter your username: ')
    if password is None:
        password = getpass.getpass('Enter your password: ')
    session = OLW.OktaSession('albertsons')
    session.okta_auth(username=username, password=password)
    return session



def get_cookies():
    session = initiate_session()
    expires = get_expire_time(session.okta_session.cookies.items)
    cookies = session.okta_session.cookies.items()
    headers = dict(session.okta_session.headers)
    return expires, cookies, headers



def get_expire_time(cookies_object):
    cookie_content = str(cookies_object).split()
    expire_time = None
    for item in cookie_content:
        if item[:7] == 'expires' and item[8:-1] != 'None':
            unix_time = item[8:-1]
            if unix_time.isdigit():
                expire_time = datetime.utcfromtimestamp(int(unix_time))
                break
    return expire_time


expires, cookies, headers = get_cookies()




import requests

def login_to_third_party(username: str, password: str) -> str:
    # Make a POST request to the login endpoint of the third-party website
    login_url = "https://albertsons.okta.com"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(login_url, data=payload)
    # Check if the login was successful
    if response.status_code == 200:
        # Store the session cookies
        expire_time = get_expire_time(response.cookies)
        session_cookies = response.cookies.get_dict()
        # Extract the JWT token from the cookies or response headers
        jwt_token = extract_jwt_token(response)
        # Store the session cookies and JWT token for further use
        store_session_cookies(session_cookies)
        store_jwt_token(jwt_token)
        return "Login successful"
    else:
        return "Login failed"


def extract_jwt_token(response: requests.Response) -> str:
    # Extract the JWT token from the cookies or response headers
    # You may need to inspect the response headers or cookies to find the JWT token
    # For example, if the JWT token is in the "Authorization" header:
    jwt_token = response.headers.get("Authorization")
    return jwt_token

def store_session_cookies(session_cookies: dict):
    # Store the session cookies for further use
    # You can store them in a variable, database, or any other storage mechanism
    # For example, storing them in a global variable:
    global stored_session_cookies
    stored_session_cookies = session_cookies

def store_jwt_token(jwt_token: str):
    # Store the JWT token for further use
    # You can store it in a variable, database, or any other storage mechanism
    # For example, storing it in a global variable:
    global stored_jwt_token
    stored_jwt_token = jwt_token