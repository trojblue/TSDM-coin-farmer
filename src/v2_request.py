"""
尝试用requests方式完成签到
"""
from datetime import datetime
import requests
from cookie import *



def work_single_post(cookie: List):
    """用post方式为一个账户打工
    cookie: List[Dict]
    """

    # 登录只需要3个cookie: sid, saltkey, auth
    cookie_serialized = "; ".join([i['name'] + "=" + i['value'] for i in cookie])

    # 必须要这个content-type, 否则没法接收
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'cookie': cookie_serialized,
        'connection': 'Keep-Alive',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.tsdm39.net/plugin.php?id=np_cliworkdz:work',
        'content-type': 'application/x-www-form-urlencoded'
    }

    r1 = requests.post(work_page, data="act=clickad", headers=headers)
    if "必须与上一次间隔" in r1.text:
        print("该账户已经打工过")
        return

    for i in range(5):  # 总共6次打工, 还剩5次
        requests.post(work_page, data="act=clickad", headers=headers)
        time.sleep(0.1)
        print("点击广告: ", i + 1, end="\r")

    r2 = requests.post(work_page, data="act=getcre", headers=headers)

    if "您已经成功领取了奖励天使币" in r2.text:
        print("打工成功")

    else:
        print(datetime.now(), "======未知原因打工失败=======")

    # todo: 保存log
    return


def work_multi_post():
    cookies = read_cookies()

    for user in cookies.keys():
        print(datetime.now(), "正在打工: ", user)
        work_single_post(cookies[user])

    print("POST方式: 全部打工完成")
    return


sign_page_with_param = 'https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1'

sign_data = "formhash=1de28352&qdxq=wl&qdmode=3&todaysay=&fastreply=1"

def sign_single_post(cookie):
    """用post方式为一个账户签到
    cookie: List[Dict]
    """
    # 登录只需要3个cookie: sid, saltkey, auth
    cookie_serialized = "; ".join([i['name'] + "=" + i['value'] for i in cookie])
    cookie_tested = cookie_serialized + 's_gkr8_f779_smile=4D1;'

    # 必须要这个content-type, 否则没法接收
    headers = {
        'accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'cookie': cookie_tested,
        'connection': 'Keep-Alive',
        'referer': 'https://www.tsdm39.net/home.php?mod=space&do=pm',
        'content-type': 'application/x-www-form-urlencoded'
    }

    r1 = requests.post(sign_page_with_param, data=sign_data, headers=headers)
    txt = r1.text
    if "恭喜你签到成功!获得随机奖励" in r1.text:
        print("签到成功")
    elif "您今日已经签到" in r1.text:
        print("该账户已经签到过")
    else:
        print(datetime.now(), "======未知原因签到失败=======")

    # todo: 保存log
    return

def sign_multi_post():
    cookies = read_cookies()

    for user in cookies.keys():
        print(datetime.now(), "正在签到: ", user)
        sign_single_post(cookies[user])

    print("POST方式: 全部签到完成")
    return


if __name__ == '__main__':
    work_multi_post()
