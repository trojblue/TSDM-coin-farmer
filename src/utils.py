from farmer import *
from selenium import webdriver
from typing import List
import pickle
import time
import os



def get_cookie(username:str, password:str):
    """selenium获取cookie
    """

    browser = webdriver.Chrome()
    browser.get(login_page)

    browser.find_element_by_xpath("//*[starts-with(@id,'username_')]").send_keys(username)
    browser.find_element_by_xpath("//*[starts-with(@id,'password3_')]").send_keys(password)

    man_verify_code = input("input verification：")

    if man_verify_code:
        browser.find_element_by_name("tsdm_verify").send_keys(man_verify_code)

    browser.find_element_by_name("loginsubmit").click()
    time.sleep(1)

    print("start dumping cookies")
    new_cookie = browser.get_cookies()

    browser.quit()
    save_cookies(new_cookie, username)
    return new_cookie

def read_cookies():
    """从文件读取cookies
    { username: [cookie] }
    """
    output_path = os.path.join(SAVE_PATH, FILENAME)
    f = open(output_path, 'rb')
    cookies = pickle.load(f)
    f.close()

    return cookies

def save_cookies(new_cookie:List, username:str) -> None:
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


def load_cookies(driver) -> None:
    """获取cookie, 并且载入浏览器
    """
    directory = os.path.dirname(SAVE_PATH)
    if not os.path.exists(directory):
        print("文件夹不存在, 获取cookie...") # TODO: 自动获取cookie
        return
    else:
        print("读取cookie....")
        cookies = read_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    return
