#!./python-env/bin/python
import os
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dotenv import load_dotenv


# load_dotenv()

def get_exists_element(driver, by, e, single=True):
    try:
        if single:
            el = driver.find_element(by, e)
        else:
            el = driver.find_elements(by, e)
    except NoSuchElementException:
        return False
    return el


def search_my_candidate(driver, url, person_id):
    driver.get(url)
    antiddos = get_exists_element(driver, By.XPATH, '//*[contains(text(), "Войти") and @href="/site/anti-ddos"]')
    if antiddos:
        antiddos.click()
        return search_my_candidate(driver, url, person_id)
    else:
        my_candidate = get_exists_element(driver, By.XPATH, f'//*[contains(text(), "{person_id}")]/../*',
                                          single=False)
        return my_candidate


def send_tg(text):
    response = get(f'https://api.telegram.org/bot{os.getenv("BOT_API")}/sendMessage',
                   params={
                       'chat_id': os.getenv("CHAT_ID"),
                       'text': text
                   })

    # Press the green button in the gutter to run the script.


def test():
    print('ok')


def do_request(url, id, columns=[0], is_original=False):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME, options=chrome_options)

    data = search_my_candidate(wd, url, id)
    if not data:
        print("!!!!! NO DATA !!!!!!")
        wd.quit()
    r = [i.text for i in data]
    wd.quit()

    result = []
    for i in columns:
        result.append(r[i])

    return result
