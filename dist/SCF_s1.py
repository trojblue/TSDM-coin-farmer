# -*- coding: utf-8 -*-

# 适配云函数, 单个文件完成s1阅读



from datetime import datetime
from typing import List
import random, requests, time, json

# ======== CONSTANT =======

s1_domain = "bbs.saraba1st.com"
s1_frontpage = "https://bbs.saraba1st.com/2b/forum.php"
s1_sample_post = "https://bbs.saraba1st.com/2b/thread-2039915-1-4.html"


# ========= COOKIE ========

def get_cookies_all():
    """从文件读取所有cookies
    { username: [cookie] }
    """
    try:
        with open('cookies.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data

    except FileNotFoundError:  # 文件不存在
        print("cookies.json不存在")
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


# ======= WORK ======


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
        print("%s S1: 状态正常"%datetime.now())
    else:
        print("%s ====S1: 状态异常===="%datetime.now())


def do_read_s1_all():
    s1_cookie = get_cookies_by_domain(s1_domain)
    print("正在s1刷在线时间...")

    for user in s1_cookie.keys():
        print("%s 正在s1阅读: %s"%(datetime.now(), user))
        try:
            do_read_s1_single(s1_cookie[user])
        except Exception as e:
            print("====S1阅读失败, 继续运行: %s==="%e)

    print("s1阅读完成")



def main_handler(event, context):
    do_read_s1_all()