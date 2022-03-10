import json
import logging

from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from lib.logger import *
from lib.cookie import *

# Local path
COOKIE_PATH = './privates/cookies.json'

# Header

HEADER_TSDM_WORK = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'cookie_list': "===CHANGE ME===",
        'connection': 'Keep-Alive',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.tsdm39.net/plugin.php?id=np_cliworkdz:work',
        'content-type': 'application/x-www-form-urlencoded'
}

HEADER_TSDM_SIGN = {
    'accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'cookie_list': "===CHANGE ME===",
    'connection': 'Keep-Alive',
    'referer': 'https://www.tsdm39.net/home.php?mod=space&do=pm',
    'content-type': 'application/x-www-form-urlencoded'
}

HEADER_S1_READ = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'cookie_list': "===CHANGE ME===",
        'connection': 'Keep-Alive',
        'referer': 'https://bbs.saraba1st.com/2b/forum-6-1.html',
}


HEADER_EAT_SIGN = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'cookie_list': "===CHANGE ME===",
        'connection': 'Keep-Alive',
        'referer': 'https://eatasmr.com/tasks/attendance',
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'content-type': "application/x-www-form-urlencoded",
        'origin': "https://eatasmr.com"
    }


# URL

tsdm_sign_url = 'https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign'
sign_url_with_param = 'https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1'

work_url = 'https://www.tsdm39.net/plugin.php?id=np_cliworkdz:work'
login_url = 'https://www.tsdm39.net/member.php?mod=logging&action=login'

s1_frontpage = "https://bbs.saraba1st.com/2b/forum.php"
s1_sample_post = "https://bbs.saraba1st.com/2b/thread-2022232-1-1.html"

# cookie_list domain
tsdm_domain = ".tsdm39.net"
s1_domain = "bbs.saraba1st.com"
eatasmr_domain = "eatasmr.com"


# re相关
re_URL = "(?P<url>https?://[^\s]+)"

def get_webdriver():
    """返回设置好参数的webdriver
    """
    options = webdriver.ChromeOptions()
    options.add_argument("disable-software-rasterizer")
    options.add_argument("log-level=3")
    driver = webdriver.Chrome(chrome_options=options)
    return driver

def get_serialized_cookie(cookie_list:List):
    return "; ".join([i['name'] + "=" + i['value'] for i in cookie_list])


def get_headers(cookie_list:List, header:Dict) -> Dict:
    """读取 <cookie_list>, 添加到 <header>
    :param cookie_list: get_cookies_by_domain()
    :param header: 在model.py设置
    :return: 完整cookie
    """
    cookie_serialized = get_serialized_cookie(cookie_list)

    headers = header
    headers['cookie_list'] = cookie_serialized
    return headers

def write_new_cookie(new_cookie: List, username: str) -> None:
    """向cookie文件写入新的用户cookie
    { username: [cookie_list] }
    """
    simplified_new_cookie = simplify_cookie(new_cookie)
    cookies = get_cookies_all(COOKIE_PATH)

    # TODO: 相同名称的直接覆盖, 不同站点的用不同cookie文件, 或者机制检测
    cookies[username] = simplified_new_cookie

    with open(COOKIE_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(cookies, json_file, ensure_ascii=False, indent=4)

    display_info("写入cookie文件完成")


def write_new_cookie_all(new_cookie: List, username: str) -> None:
    """写入所有新的用户cookie
    { username: [cookie_list] }
    """
    cookies = get_cookies_all(COOKIE_PATH)
    # TODO: 相同名称的直接覆盖, 不同站点的用不同cookie文件, 或者机制检测
    cookies[username] = new_cookie

    with open(COOKIE_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(cookies, json_file, ensure_ascii=False, indent=4)

    display_info("写入cookie文件完成")


def simplify_cookie(cookie):
    """只保存登录需要的2个cookie: saltkey, auth
    """
    simplified_cookie = []
    login_word = ['_saltkey', '_auth', 'EATSESSID',
                  'wordpress_logged_in_bbae6ecd47232ff70d42a5fbe3863254']
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