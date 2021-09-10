"""
DLC: s1论坛自动浏览刷时间功能
"""
import random
import time

import requests

from actions import *

s1_frontpage = "https://bbs.saraba1st.com/2b/forum.php"
s1_sample_post = "https://bbs.saraba1st.com/2b/thread-2022232-1-1.html"

def refresh_cookie_s1(username: str, password:str):
    """selenium获取单个S1 cookie
    """
    driver = get_webdriver()
    driver.get(s1_frontpage)
    driver.find_element_by_id("ls_cookietime").click()

    if username and password:
        # 存在S1_CREDENTIALS, 自动填入密码登录
        driver.find_element_by_id("ls_username").send_keys(username)
        driver.find_element_by_id("ls_password").send_keys(password)
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id=\"lsform\"]/div/div/table/tbody/tr[2]/td[3]/button").click()
        print("自动登录:")
        time.sleep(4)  # 增加延迟确保获得auth

    else:
        print("刷新cookie: 未找到S1_CREDENTIALS, 想要自动获取cookie请按readme设置好该变量")
        wait_input = input("请填入账号密码, 点击登录后按回车")

    if not username:
        # 无s1_CREDENTIAL, 从浏览器获取用户名
        my_username = driver.find_element_by_xpath("//*[@id='um']/p[1]/strong/a").text
        assert my_username is not None
    else:
        my_username = username

    new_cookie = driver.get_cookies()
    driver.close()

    print("正在写入cookie..")
    write_new_cookie_s1(new_cookie, my_username)
    return new_cookie


def refresh_cookies_s1():
    """从credentials重新获取所有cookie
    ===仅测试过单账户使用===
    """
    try:
        # 多账户刷新
        from settings import S1_CREDENTIALS
        for i in S1_CREDENTIALS:
            refresh_cookie_tsdm(i[0], i[1])

    except ImportError:
        print("未找到S1_credentials, 为单个账户手动刷新cookie; \n"
              "如果需要多账户签到/自动填写密码, 请先按照readme设置好账户密码")
        refresh_cookie_s1("", "")

    return


def write_new_cookie_s1(new_cookie: List, username: str) -> None:
    """向cookie文件写入新的用户cookie
    { username: [cookie] }
    """
    cookies = get_cookies_all()
    cookies[username] = simplify_cookie(new_cookie)

    with open('cookies.json', 'w', encoding='utf-8') as json_file:
        json.dump(cookies, json_file, ensure_ascii=False, indent=4)

    print("write done")

def do_read_s1_single(cookie:List):
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
        print(datetime.now(), "====S1: 状态异常====")


def do_read_s1_all():
    s1_cookie = get_cookies_by_domain(s1_domain)
    print("正在s1刷在线时间...")

    for user in s1_cookie.keys():
        print(datetime.now(), "正在s1阅读: ", user)
        try:
            do_read_s1_single(s1_cookie[user])
        except Exception:
            print(datetime.now(), "====阅读失败, 继续运行===")

    print("s1阅读完成")
