"""
DLC: s1论坛自动浏览刷时间功能
"""
import random
import time

import requests

from actions import *
from credentials import S1_CREDENTIALS

s1_frontpage = "https://bbs.saraba1st.com/2b/forum.php"
s1_sample_post = "https://bbs.saraba1st.com/2b/thread-2022232-1-1.html"

def get_s1_cookie():
    """selenium获取cookie
    """

    username, password = S1_CREDENTIALS[0][0], S1_CREDENTIALS[0][1]

    driver = get_webdriver()
    driver.get(s1_frontpage)

    driver.find_element_by_id("ls_username").send_keys(username)
    driver.find_element_by_id("ls_password").send_keys(password)
    driver.find_element_by_id("ls_cookietime").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id=\"lsform\"]/div/div/table/tbody/tr[2]/td[3]/button").click()

    print("登录:")
    time.sleep(4)   # 增加延迟确保获得auth

    new_cookie = driver.get_cookies()
    driver.close()

    write_new_s1_cookie(new_cookie, username)
    return new_cookie


def write_new_s1_cookie(new_cookie: List, username: str) -> None:
    """向cookie文件写入新的用户cookie
    { username: [cookie] }
    """
    simplified_new_cookie = simplify_cookie(new_cookie)
    cookies = {}
    cookies[username] = simplified_new_cookie

    with open('cookies_s1.json', 'w', encoding='utf-8') as json_file:
        json.dump(cookies, json_file, ensure_ascii=False, indent=4)

    print("write done")


def read_post(cookie:List):
    """浏览一个帖子
    """
    cookie_serialized = "; ".join([i['name'] + "=" + i['value'] for i in cookie])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'cookie': cookie_serialized,
        'connection': 'Keep-Alive',
        'referer': 'https://bbs.saraba1st.com/2b/forum-6-1.html',
    }

    read_response = requests.get(s1_sample_post, headers=headers)

    if ("动漫论坛 -  Stage1st") in read_response.text:
        print(datetime.now(), "S1: 状态正常")
    else:
        print(datetime.now(), "S1: 状态异常")

def read_cookies_s1():
    """从文件读取cookies
    { username: [cookie] }
    """
    try:
        with open('cookies_s1.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data

    except FileNotFoundError:  # 文件不存在
        print("cookies.json不存在")
        return {}


def do_read_s1():
    s1_cookie = read_cookies_s1()
    print("正在s1假装阅读...")

    for user in s1_cookie.keys():
        print(datetime.now(), "正在s1阅读: ", user)
        read_post(s1_cookie[user])

    print("s1阅读完成")
