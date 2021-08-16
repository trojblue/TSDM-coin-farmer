import json
import time
from typing import List

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from credentials import TSDM_credentials
from datetime import datetime


sign_url = 'https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign'
work_url = 'https://www.tsdm39.net/plugin.php?id=np_cliworkdz:work'
login_url = 'https://www.tsdm39.net/member.php?mod=logging&action=login'

COOKIE_FILE = 'cookies.pickle'

def get_webdriver():
    """返回设置好参数的webdriver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def get_cookie(username: str, password: str):
    """selenium获取cookie
    """
    driver = get_webdriver()
    driver.get(login_url)

    driver.find_element_by_xpath("//*[starts-with(@id,'username_')]").send_keys(username)
    driver.find_element_by_xpath("//*[starts-with(@id,'password3_')]").send_keys(password)
    driver.find_element_by_xpath("//*[starts-with(@id,'cookietime_')]").click()
    driver.find_element_by_name("tsdm_verify").click()

    print("等待浏览器里填写验证码并登录:")
    wait = WebDriverWait(driver, 100)
    wait.until(EC.title_contains("提示信息 - "))

    new_cookie = driver.get_cookies()
    driver.quit()

    write_new_cookie(new_cookie, username)
    return new_cookie


def read_cookies():
    """从文件读取cookies
    { username: [cookie] }
    """
    try:
        with open('cookies.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data

    except FileNotFoundError:  # 文件不存在
        return {}


def write_new_cookie(new_cookie: List, username: str) -> None:
    """向cookie文件写入新的用户cookie
    { username: [cookie] }
    """

    simplified_new_cookie = simplify_cookie(new_cookie)
    cookies = read_cookies()
    cookies[username] = simplified_new_cookie
    # cookies[username] = new_cookie

    with open('cookies.json', 'w', encoding='utf-8') as json_file:
        json.dump(cookies, json_file, ensure_ascii=False, indent=4)

    print("write done")


def simplify_cookie(cookie):
    """只留下登录所需的3个cookie
    登录只需要3个cookie: sid, saltkey, auth
    签到需要的可能不一样
    """
    simplified_cookie = []
    # login_word = ['_saltkey', '_sid', '_auth']
    login_word = ['_saltkey', '_auth']
    for i in cookie:
        if any(word in i['name'] for word in login_word):
            simplified_cookie.append(i)

    return simplified_cookie


def refresh_all_cookies(credentials):
    """从credentials获取所有cookie
    用之前记得删掉原有的cookies.pickle
    """
    for i in credentials:
        get_cookie(i[0], i[1])
    return


def update_new_accounts():
    """根据TSDM_credentials,
    添加新的cookie, 但是不刷新老账户
    """
    usernames = read_cookies().keys()
    new_cred = []

    for cred in TSDM_credentials:
        if cred[0] not in usernames:
            new_cred.append(cred)

    print("添加", len(new_cred), "个新账户:")
    refresh_all_cookies(new_cred)
    return


def write_error(prefix:str, content:str):
    """prefix: 文件名前缀
    content: 错误日志内容
    """
    with open(prefix + str(datetime.now()) + '.txt', 'w') as f:
        f.write(content)


if __name__ == '__main__':
    refresh_all_cookies(TSDM_credentials)