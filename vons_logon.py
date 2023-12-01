from oktaloginwrapper import OktaLoginWrapper as OLW
import getpass

def initiate_session():
    user_name = input('Enter your username: ')
    password = getpass.getpass('Enter your password: ')
    session = OLW.OktaSession('albertsons')
    session.okta_auth(username=user_name, password=password)
    return session


def get_cookies():
    session = initiate_session()
    cookies = session.okta_session.cookies.items()
    headers = session.okta_session.headers