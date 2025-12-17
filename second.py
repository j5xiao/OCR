import time
import re
import tesserocr
from selenium import webdriver
from io import BytesIO
from PIL import Image
from retrying import retry
import numpy as np
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def preprocess(image):
    image = image.convert('L')
    array = np.array(image)
    array = np.where(array > 50, 255, 0)
    image = Image.fromarray(array.astype('uint8'))
    return image

@retry(stop_max_attempt_number=50, retry_on_result=lambda x: x is False)
def login():
    try:
        browser.get('https://captcha7.scrape.center/')
        WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, '#captcha'))
        )

        # Fill username/password
        browser.find_element(By.CSS_SELECTOR, '.username input[type=text]').send_keys('admin')
        browser.find_element(By.CSS_SELECTOR, '.password input[type=password]').send_keys('admin')

        # Get captcha and OCR
        captcha_element = browser.find_element(By.CSS_SELECTOR, '#captcha')
        image = Image.open(BytesIO(captcha_element.screenshot_as_png))
        captcha_text = preprocess(image)
        captcha_text = re.sub('[^A-Za-z0-9]', '', captcha_text)

        browser.find_element(By.CSS_SELECTOR, '.captcha input[type=text]').send_keys(captcha_text)
        browser.find_element(By.CSS_SELECTOR, '.login').click()

        WebDriverWait(browser, 10).until(
            ec.presence_of_element_located((By.XPATH, '//h2[contains(.,"登录成功")]'))
        )
        browser.quit()
        return True
    except TimeoutException:
        return False
    
if __name__ == '__main__':
    browser = webdriver.Chrome()
    login()
