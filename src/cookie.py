import os
import pickle
import time
from typing import List
from selenium import webdriver
from credentials import TSDM_credentials

sign_page = 'https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign'
work_page = 'https://www.tsdm39.net/plugin.php?id=np_cliworkdz:work'
login_page = 'https://www.tsdm39.net/member.php?mod=logging&action=login'

SAVE_PATH = '../bin'
FILENAME = 'cookies.pickle'


def get_cookie(username: str, password: str):
    """selenium获取cookie
    """
    browser = webdriver.Chrome()
    browser.get(login_page)

    browser.find_element_by_xpath("//*[starts-with(@id,'username_')]").send_keys(username)
    browser.find_element_by_xpath("//*[starts-with(@id,'password3_')]").send_keys(password)

    man_verify_code = input("input verification：")

    if man_verify_code:  # 没输入, 默认手动填好了
        browser.find_element_by_name("tsdm_verify").send_keys(man_verify_code)
        browser.find_element_by_name("loginsubmit").click()
        time.sleep(1)

    print("start dumping cookies")
    new_cookie = browser.get_cookies()
    browser.quit()

    add_cookie(new_cookie, username)
    return new_cookie


def read_cookies():
    """从文件读取cookies
    { username: [cookie] }
    """
    output_path = os.path.join(SAVE_PATH, FILENAME)
    try:
        f = open(output_path, 'rb')
        cookies = pickle.load(f)
        f.close()
        return cookies

    except FileNotFoundError:  # 文件不存在
        return {}


def add_cookie(new_cookie: List, username: str) -> None:
    """向cookie文件写入新的用户cookie
    { username: [cookie] }
    """
    directory = os.path.dirname(SAVE_PATH)
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_path = os.path.join(SAVE_PATH, FILENAME)

    cookies = read_cookies()
    cookies[username] = new_cookie

    f = open(output_path, 'wb')
    pickle.dump(cookies, f)
    f.close()
    print("write done")


def get_multiple_cookie(credentials):
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
    get_multiple_cookie(new_cred)
    return
