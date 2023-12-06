from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


options = Options()
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
options.add_argument("--headless")
options.add_argument("--start-maximized")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.vons.com")

all_cookies = driver.get_cookies()
logs = driver.get_log("performance")



driver.get("https://www.vons.com/ueene-suffe-and-swort-it-know-tenda-Enter-I-dist")

all_cookies = driver.get_cookies()
logs = driver.get_log("performance")
#driver.close()



def initiate_okta():
    url = 'https://albertsons.okta.com/api/v1/sessions/me/lifecycle/refresh'
    headers = {
        ':authority:': 'albertsons.okta.com',
        ':method:': 'POST',
        ':path:': '/api/v1/sessions/me/lifecycle/refresh',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Length': '0',
        'Origin': 'https://www.vons.com/',
        'Referer': 'https://www.vons.com/',
        'Sec-Ch-Ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Gpc': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    response = requests.post(url=url, headers=headers)




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


def step_one():
    visid_incap, incap_ses, incap_res = None, None, None
    headers = initial_headers()
    response = requests.get(url='https://www.vons.com', headers=headers)
    incap_res = find_item(response.text, '_Incapsula_Resource?')[2:]
    cookies = response.headers.get('Set-Cookie').split()
    for cookie in cookies:
        if cookie[:12] == 'visid_incap_':
            visid_incap = cookie
        elif cookie[:12] == 'nlbi_1610354':
            nlbi = cookie
        elif cookie[:9] == 'incap_ses':
            incap_ses = cookie
    return visid_incap, incap_ses, incap_res

visid_incap, incap_ses, incap_res = step_one()


def step_two(visid_incap, incap_ses, incap_res):
    headers = headers()
    cookie_string = combine_cookies([visid_incap, incap_ses])


def combine_cookies(all_cookies):
    cookie_string = ''
    for item in all_cookies:
        if len(cookie_string) != 0:
            cookie_string += '; '
        cookie_string += item
    return cookie_string


def find_item(text, criteria):
    matched_item = None
    items = text.split('"')
    for item in items:
        if criteria in item:
            matched_item = item
            break
    return matched_item


def fix_json(jsonStr):
    # Remove all empty spaces to make things easier bellow
    jsonStr = jsonStr.replace('" :','":').replace(': "',':"').replace('"\n','"').replace('" ,','",').replace(', "',',"')
    # First remove the " from where it is supposed to be.
    jsonStr = re.sub(r'\\"', '"', jsonStr)
    jsonStr = re.sub(r'{"', '{`', jsonStr)
    jsonStr = re.sub(r'"}', '`}', jsonStr)
    jsonStr = re.sub(r'":"', '`:`', jsonStr)
    jsonStr = re.sub(r'":\[', '`:[', jsonStr)
    jsonStr = re.sub(r'":\{', '`:{', jsonStr)
    jsonStr = re.sub(r'":([0-9]+)', '`:\\1', jsonStr)
    jsonStr = re.sub(r'":([null|true|false])', '`:\\1', jsonStr)
    jsonStr = re.sub(r'","', '`,`', jsonStr)
    jsonStr = re.sub(r'",\[', '`,[', jsonStr)
    jsonStr = re.sub(r'",\{', '`,{', jsonStr)
    jsonStr = re.sub(r',"', ',`', jsonStr)
    jsonStr = re.sub(r'\["', '[`', jsonStr)
    jsonStr = re.sub(r'"\]', '`]', jsonStr)
    # Backslash all double quotes (")
    jsonStr = re.sub(r'"','\\"', jsonStr)
    # Put back all the " where it is supposed to be.
    jsonStr = re.sub(r'\`','\"', jsonStr)
    return jsonStr