import json
import logging

from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from logger import *


sign_url = 'https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign'
work_url = 'https://www.tsdm39.net/plugin.php?id=np_cliworkdz:work'
login_url = 'https://www.tsdm39.net/member.php?mod=logging&action=login'

# cookie domain
tsdm_domain = ".tsdm39.net"
s1_domain = "bbs.saraba1st.com"

def get_webdriver():
    """返回设置好参数的webdriver
    """
    options = webdriver.ChromeOptions()
    options.add_argument("disable-software-rasterizer")
    options.add_argument("log-level=3")
    driver = webdriver.Chrome(chrome_options=options)
    return driver


def refresh_cookie_tsdm(username: str, password: str):
    """selenium获取cookie
    """
    add_debug("刷新cookie")
    driver = get_webdriver()
    driver.get(login_url)
    driver.find_element_by_xpath("//*[starts-with(@id,'cookietime_')]").click()

    if username and password: # 账户密码非空
        driver.find_element_by_xpath("//*[starts-with(@id,'username_')]").send_keys(username)
        driver.find_element_by_xpath("//*[starts-with(@id,'password3_')]").send_keys(password)
        driver.find_element_by_name("tsdm_verify").click()
        display_info("等待浏览器里填写验证码并登录:")
    else:
        # 无TSDM_CREDENTIAL, 手动填写信息
        display_warning("请手动填写信息后点击登录:")

    wait = WebDriverWait(driver, 100)
    wait.until(EC.title_contains("提示信息 - "))

    if not username:
        # 无TSDM_CREDENTIAL, 从浏览器获取用户名
        my_username = driver.find_element_by_xpath("//*[@id='um']/p[1]/strong/a").text
        assert my_username is not None
    else:
        my_username = username

    new_cookie = driver.get_cookies()
    driver.close()

    write_new_cookie(new_cookie, my_username)
    return new_cookie

def refresh_cookies_tsdm():
    """从credentials重新获取所有cookie
    """
    try:
        # 多账户刷新
        from settings import TSDM_CREDENTIALS
        for i in TSDM_CREDENTIALS:
            refresh_cookie_tsdm(i[0], i[1])

    except ImportError:
        display_warning("未找到TSDM_credentials, 为单个账户手动刷新cookie; \n"
              "如果需要多账户签到/自动填写密码, 请先按照readme设置好天使动漫的账户密码")
        refresh_cookie_tsdm("", "")

    return


def get_cookies_all():
    """从文件读取所有cookies
    { username: [cookie] }
    """
    try:
        with open('cookies.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data

    except FileNotFoundError:  # 文件不存在
        display_warning("cookies.json不存在")
        return {}


def get_cookies_by_domain(domain:str):
    """从所有cookie里分离出指定域名的cookie
    domain: cookie domain, (".tsdm39.net")
    """
    cookies_all = get_cookies_all() #     { username: [cookie] }
    domain_cookies = {}

    for username in cookies_all.keys():
        curr_user_cookies = cookies_all[username]
        curr_user_cookies_domained = []

        # 同一个用户名下可能有多个网站的cookie
        for cookie in curr_user_cookies:
            if cookie['domain'] == domain:
                curr_user_cookies_domained.append(cookie)

        if curr_user_cookies_domained != []:
            domain_cookies[username] = curr_user_cookies_domained

    return domain_cookies



def write_new_cookie(new_cookie: List, username: str) -> None:
    """向cookie文件写入新的用户cookie
    { username: [cookie] }
    """
    simplified_new_cookie = simplify_cookie(new_cookie)
    cookies = get_cookies_all()
    cookies[username] = simplified_new_cookie

    with open('cookies.json', 'w', encoding='utf-8') as json_file:
        json.dump(cookies, json_file, ensure_ascii=False, indent=4)

    display_info("写入cookie文件完成")


def simplify_cookie(cookie):
    """只保存登录需要的2个cookie: saltkey, auth
    """
    simplified_cookie = []
    login_word = ['_saltkey', '_auth']
    for i in cookie:
        if any(word in i['name'] for word in login_word):
            simplified_cookie.append(i)

    return simplified_cookie



def write_error(prefix:str, content:str):
    """保存错误日志
    prefix: 文件名前缀
    content: 错误日志内容
    """
    my_date = prefix + datetime.today().strftime(' %Y-%m-%d %H%M %S.%f.log')
    with open(my_date, "w") as f:
        f.write(content)
    return