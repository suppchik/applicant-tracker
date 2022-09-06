#!./python-env/bin/python
import os
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dotenv import load_dotenv

load_dotenv()


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


if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage') 
    wd = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME, options=chrome_options)
    candidate_id = os.getenv("CANDIDATE_ID") 
    candidates_url = os.getenv("CANDIDATES_URL") 
    data = search_my_candidate(wd, candidates_url, candidate_id)
    if not data:
        print("!!!!! NO DATA !!!!!!")
        wd.quit()
    r = [i.text for i in data]
    message = [
        f'Место в списке: {r[0]}',
        f'Сумма баллов: {r[9]} б.'
    ]
    print('\n'.join(message))
    wd.quit()

