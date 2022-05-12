import pyotp, time

from kiteconnect import KiteTicker, KiteConnect

from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller

from datetime import datetime

now = datetime.now()


def selenium_kite_login(API_KEY_1, CLIENT_ID_1, PASSWORD_1, TOTP_KEY_1, API_SECRET_1):
    try:
        options = Options()
        options.add_argument('--headless')  # Disable the ui
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chromedriver_autoinstaller.install(), chrome_options=options)

        kite = KiteConnect(api_key=API_KEY_1)
        login_url = kite.login_url()
        driver.get(login_url)
        time.sleep(2)

        userid = driver.find_element(By.XPATH, '//*[@id="userid"]')
        userid.send_keys(CLIENT_ID_1)

        password = driver.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys(PASSWORD_1)

        login_button = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div/form/div[4]/button')
        login_button.click()
        time.sleep(2)

        tpin = driver.find_element(By.XPATH, '//*[@id="totp"]')
        totp = pyotp.TOTP(TOTP_KEY_1)
        tpin.send_keys(totp.now())
        submit_button = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div[2]/form/div[3]/button')
        submit_button.click()
        time.sleep(2)

        current_url = driver.current_url
        parse_url = urlparse(current_url)
        request_token = parse_qs(parse_url.query)['request_token'][0]
        driver.quit()

        # **** Set Access_token
        access_token = kite.generate_session(request_token, api_secret=API_SECRET_1)["access_token"]
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        kite.set_access_token(access_token)
        autologin = 'SUCCESS'
        return [access_token, dt_string, autologin, kite]

    except Exception as e:
        access_token = None
        dt_string = None
        autologin = 'FAILED'
        return [access_token, dt_string, autologin]

# API_KEY = "wbxs1zv79wglv0rb"
# Client_ID = "ZK1113"
# Password = "Ashwini@3112"
# Totp = "QJDQ35DV6HZFLBSYTNYTYONLJLGRTOHF"
# API_secret = "93z0av6ddxqph1k0vrflbm80n3qh79fw"
#
# datta = selenium_kite_login(API_KEY, Client_ID, Password, Totp, API_secret)
# print(datta)
#
# print(datta['obj'], datta['access_token'])
#
# print(datta['obj'].profile())
