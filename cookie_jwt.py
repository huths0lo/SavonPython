from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get('http://selenium.dev')
driver.quit()



browser = webdriver.Firefox()
browser.get('http://selenium.dev/')