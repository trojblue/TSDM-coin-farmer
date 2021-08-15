"""
尝试用requests方式完成签到
"""

import requests
import sys
import traceback
from cookie import *



def work_single(cookie:List):
    """用post方式为一个账户打工
    cookie: List[Dict]
    """
    cookie_serialized = "; ".join([i['name']+"="+i['value'] for i in cookie])

    # 必须要这个content-type, 否则没法接收
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'cookie': cookie_serialized,
        'connection': 'Keep-Alive',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.tsdm39.net/plugin.php?id=np_cliworkdz:work',
        'content-type': 'application/x-www-form-urlencoded'
    }

    for i in range (6):
        requests.post(work_page, data="act=clickad", headers=headers)
        time.sleep(0.1)
        print("点击广告: ", i+1, end="\r")

    response = requests.post(work_page, data="act=getcre", headers=headers)

    if "您已经成功领取了奖励天使币" in response.text:
        print("打工成功")
    elif "必须与上一次间隔" in response.text:
        print("该账户已经打工过")
    else:
        print("======未知原因打工失败=======")

    # todo: 保存log
    return


def work_multi():
    all_cookies = list(read_cookies().values())

    for i in all_cookies:
        work_single(i)

    print("POST方式: 全部打工完成")
    return


if __name__ == '__main__':
    work_multi()



