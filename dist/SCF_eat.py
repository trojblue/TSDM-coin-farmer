from datetime import datetime
from typing import *
import random, requests, time, json


eat_login_url = "https://eatasmr.com/community"
eat_attendance_url = "https://eatasmr.com/tasks/attendance"
eat_sign_url_without_formhash = "https://eatasmr.com/tasks/attendance?a=check&__v="
eatasmr_domain = "eatasmr.com"

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

def write_new_cookie_all(new_cookie: List, username: str) -> None:
    """写入所有新的用户cookie
    { username: [cookie] }
    """
    cookies = get_cookies_all()
    # TODO: 相同名称的直接覆盖, 不同站点的用不同cookie文件, 或者机制检测
    cookies[username] = new_cookie

    with open('cookies.json', 'w', encoding='utf-8') as json_file:
        json.dump(cookies, json_file, ensure_ascii=False, indent=4)

    print("写入cookie文件完成")


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



# =================================



def do_sign_eat_single(cookie:List):
    """浏览一个帖子
    """
    cookie_serialized = "; ".join([i['name'] + "=" + i['value'] for i in cookie])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'cookie': cookie_serialized,
        'connection': 'Keep-Alive',
        'referer': 'https://eatasmr.com/tasks/attendance',
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'content-type': "application/x-www-form-urlencoded",
        'origin': "https://eatasmr.com"
    }
    s = requests.session()

    sign_response = s.get(eat_attendance_url, headers=headers).text

    if ("过去30天中, 我连续签到了") in sign_response:
        print("可能登录成功")

    # if("class=\"nav__title\">🔑 登錄</span>") in sign_response:
    #     print("可能登录失败")


    if ("/tasks/attendance?a=check&__v=") in sign_response:
        form_start = sign_response.find("/tasks/attendance?a=check&__v=") + 30  # 此处30个字符
        formhash = sign_response[form_start:form_start + 10]  # formhash 10位, 保留15
        complete_url = eat_sign_url_without_formhash + formhash
        formdata = "check=%E7%B0%BD%E5%88%B0"  # URL-encoded "簽到"
        sign_response2 = s.post(complete_url, data=formdata, headers=headers)


    print("WAIT")

def do_read_eat_all():
    eat = get_cookies_by_domain(eatasmr_domain)
    print("正在eatASMR签到...")

    for user in eat.keys():
        print("%s eatASMR签到: %s"%(datetime.now(), user))
        do_sign_eat_single(eat[user])

    print("eatASMR签到完成")

if __name__ == '__main__':
    do_read_eat_all()
    # refresh_cookies_eatasmr()