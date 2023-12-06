from __future__ import absolute_import

import re
import logging
import datetime
import random
from six.moves.urllib.parse import quote, urlsplit

from requests import Session

from .parsers import WebsiteResourceParser, IframeResourceParser
from .errors import RecaptchaBlocked, MaxRetriesExceeded

logger = logging.getLogger('incapsula')


o = [
    ('navigator', 'true'),
    ('navigator.vendor', 'Google Inc.'),
    ('navigator.appName', 'Netscape'),
    ('navigator.plugins.length==0', 'false'),
    ('navigator.platform', 'Linux x86_64'),
    ('navigator.webdriver', 'undefined'),
    ('plugin_ext', 'no extention'),
    ('plugin_ext', 'so'),
    ('ActiveXObject', 'false'),
    ('webkitURL', 'true'),
    ('_phantom', 'false'),
    ('callPhantom', 'false'),
    ('chrome', 'true'),
    ('yandex', 'false'),
    ('opera', 'false'),
    ('opr', 'false'),
    ('safari', 'false'),
    ('awesomium', 'false'),
    ('puffinDevice', 'false'),
    ('__nightmare', 'false'),
    ('_Selenium_IDE_Recorder', 'false'),
    ('document.__webdriver_script_fn', 'false'),
    ('document.$cdc_asdjflasutopfhvcZLmcfl_', 'false'),
    ('process.version', 'false'),
    ('navigator.cpuClass', 'false'),
    ('navigator.oscpu', 'false'),
    ('navigator.connection', 'false'),
    ('window.outerWidth==0', 'false'),
    ('window.outerHeight==0', 'false'),
    ('window.WebGLRenderingContext', 'true'),
    ('document.documentMode', 'undefined'),
    ('eval.toString().length', '33')
]


def simple_digest(s):
    res = 0
    for ch in s:
        res += ord(ch)
    return str(res)


class IncapSession(Session):
    def __init__(self, max_retries=3, user_agent=None, cookie_domain='', resource_parser=WebsiteResourceParser,
                 iframe_parser=IframeResourceParser):
        super(IncapSession, self).__init__()

        default_useragent = 'IncapUnblockSession (https://github.com/ziplokk1/incapsula-cracker-py3)'
        user_agent = user_agent or default_useragent

        self.max_retries = max_retries
        self.cookie_domain = cookie_domain
        self.headers['User-Agent'] = user_agent

        self.ResourceParser = resource_parser
        self.IframeParser = iframe_parser

    def _get_session_cookies(self):
        return [cookie.value for cookie in self.cookies if cookie.name.startswith('incap_ses_')]

    def _create_cookie(self, name, value, seconds, domain=''):
        expires = None
        if seconds:
            d = datetime.datetime.now()
            d += datetime.timedelta(seconds=seconds)
            expires = round((d - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        self.cookies.set(name, value, domain=domain, path='/', expires=expires)

    def _set_incap_cookie(self, v_array, domain='', sl=None):
        cookies = self._get_session_cookies()
        digests = []
        for cookie_val in cookies:
            digests.append(simple_digest(v_array + cookie_val))
        dd = ','.join(digests)
        asl = self._get_incapsula_asl(dd, sl)
        res = v_array + ',digest=' + dd + ",s=" + asl
        logger.debug('setting ___utmvc cookie to {}'.format(res))
        self._create_cookie('___utmvc', res, 20, domain=domain)

    def _raise_for_recaptcha(self, resource):
        # Get the content from the iframe.
        iframe_response = self.get(resource.incapsula_iframe_url, bypass_crack=True)
        iframe_resource = self.IframeParser(iframe_response)

        if iframe_resource.is_blocked():
            raise RecaptchaBlocked(iframe_response, 'resource blocked by re-captcha')

    def _get_incapsula_b(self, incapsula_script_url):
        response = self.get(incapsula_script_url, bypass_crack=True)
        b_search = re.search(r"var b=\"(.*?)\"", response.text)
        if not b_search:
            return None
        return b_search.group(1)

    def _get_incapsula_sl(self, b):
        if not b:
            return None
        char_list = []
        for i in range(0, len(b), 2):
            char_list.append(int(b[i:i + 2], base=16))
        code = ""
        for char in char_list:
            code = code + chr(char)
        sl_search = re.search('sl = "(.+)";', code)
        if sl_search:
            return sl_search.group(1)
        return None

    def _get_incapsula_asl(self, dd, sl):
        asl = ""
        for i in range(0, len(sl)):
            asl = asl + format(ord(sl[i]) + ord(dd[i % len(dd)]), 'x')
        return asl

    def _apply_cookies(self, original_url, incapsula_script_url):
        split = urlsplit(original_url)
        scheme = split.scheme
        host = split.netloc
        b = self._get_incapsula_b(scheme + '://' + host + incapsula_script_url)
        sl = self._get_incapsula_sl(b)
        if sl:
            # Set the cookie then send request to incap resource to "apply" cookie.
            self._set_incap_cookie(test(), self.cookie_domain or host, sl)
            self.get(self.get_incapsula_resource_url(scheme, host), bypass_crack=True)

    def get_incapsula_resource_url(self, scheme, host):
        rdm = random.random()
        return scheme + '://' + host + '/_Incapsula_Resource?SWKMTFSR=1&e={}'.format(rdm)

    def crack(self, resp, org=None, tries=0):
        # Use to hold the original request so that when attempting the new unblocked request, we have a reference
        # to the original url.
        org = org or resp
        # Return original response after too many tries to bypass incap.
        # If max_retries is None then this part will never get executed allowing a continuous retry.
        if self.max_retries is not None and tries >= self.max_retries:
            raise MaxRetriesExceeded(resp, 'max retries exceeded when attempting to crack incapsula')
        resource = self.ResourceParser(resp)
        if resource.is_blocked():
            logger.debug('Resource is blocked. attempt={} url={}'.format(tries, resp.url))
            # Raise if the response content's iframe contains a recaptcha.
            self._raise_for_recaptcha(resource)
            # Apply cookies and send GET request to apply them.
            self._apply_cookies(org.url, resource.incapsula_script_url)
            # Recursively call crack() again since if the request isn't blocked after the above cookie-set and request,
            # then it will just return the unblocked resource.
            return self.crack(self.get(org.url, bypass_crack=True), org=org, tries=tries + 1)
        return resp

    def get(self, url, bypass_crack=False, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        # If the request is to get the incapsula resources, then we dont call crack().
        if bypass_crack:
            return self.request('GET', url, **kwargs)
        return self.crack(self.request('GET', url, **kwargs))