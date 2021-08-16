"""
尝试用requests方式完成签到
"""
from datetime import datetime
import requests
from actions import *



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

    ad_feedback = requests.post(work_url, data="act=clickad", headers=headers)
    if "必须与上一次间隔" in ad_feedback.text:
        print("该账户已经打工过")
        return

    for i in range(7):  # 总共6次打工, 实际打工8次保险
        ad_feedback = requests.post(work_url, data="act=clickad", headers=headers)
        time.sleep(1)
        print("点击广告: ", i + 1, end="\r")

    getcre_response = requests.post(work_url, data="act=getcre", headers=headers)

    if "您已经成功领取了奖励天使币" in getcre_response.text:
        print("打工成功")
    elif "作弊" in getcre_response.text:
        print("作弊判定, 打工失败, 重试...")
        # todo: 增加重试逻辑
    else:
        print(datetime.now(), "======未知原因打工失败, 已保存log=======")
        write_error("打工", getcre_response.text)

    return


def work_multi_post():
    cookies = read_cookies()

    for user in cookies.keys():
        print(datetime.now(), "正在打工: ", user)
        work_single_post(cookies[user])

    print("POST方式: 全部打工完成")
    return


sign_page_with_param = 'https://www.tsdm39.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1'


def sign_single_post_v2(cookie):
    cookie_serialized = "; ".join([i['name'] + "=" + i['value'] for i in cookie])

    # 必须要这个content-type, 否则没法接收
    headers = {
        'accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'cookie': cookie_serialized,
        'connection': 'Keep-Alive',
        'referer': 'https://www.tsdm39.net/home.php?mod=space&do=pm',
        'content-type': 'application/x-www-form-urlencoded'
    }

    s = requests.session()
    sign_response = s.get(sign_url, headers=headers).text

    form_start = sign_response.find("formhash=")+9 # 此处9个字符
    formhash = sign_response[form_start:form_start+8] # formhash 8位,

    sign_data = "formhash="+formhash+"&qdxq=wl&qdmode=3&todaysay=&fastreply=1" # formhash, 签到心情, 签到模式(不发言)

    sign_response = s.post(sign_page_with_param, data=sign_data, headers=headers)

    if "恭喜你签到成功!获得随机奖励" in sign_response.text:
        print("签到成功")
    elif "您今日已经签到" in sign_response.text:
        print("该账户已经签到过")
    elif "未定义操作" in sign_response.text:
        print(datetime.now(), "签到失败, 可能是formhash获取错误")
        write_error("签到", sign_response.text)
    else:
        print(datetime.now(), "======未知原因签到失败=======")
        write_error("签到", sign_response.text)

    return



def sign_multi_post():
    cookies = read_cookies()

    for user in cookies.keys():
        print(datetime.now(), "正在签到: ", user)
        sign_single_post_v2(cookies[user])

    print("POST方式: 全部签到完成")
    return


if __name__ == '__main__':
    sign_multi_post()
