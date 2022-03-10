"""
尝试用requests方式完成签到
"""
from datetime import datetime
from typing import List

import random, requests, time

from lib.model import *
from lib.logger import *
from lib.model import *


def work_single_post(cookie: List):
    """用post方式为一个账户打工
    cookie_list: List[Dict]
    """
    headers = get_headers(cookie, HEADER_TSDM_WORK)

    # 打工之前必须访问过一次网页
    page_feedback = requests.get(work_url, headers=headers)

    ad_feedback = requests.post(work_url, data="act=clickad", headers=headers)
    if "必须与上一次间隔" in ad_feedback.text:
        display_info("该账户已经打工过")
        return

    for i in range(7):  # 总共6次打工, 实际打工8次保险
        ad_feedback = requests.post(work_url, data="act=clickad", headers=headers)

        wait_time = round(random.uniform(0.5, 1), 2)
        print("点击广告: 第%s次, 等待%s秒, 服务器标识:%s" % (i + 2, wait_time, ad_feedback.text), end="\r")
        add_debug("点击广告: 第%s次, 等待%s秒, 服务器标识:%s" % (i + 2, wait_time, ad_feedback.text))
        time.sleep(wait_time)

        if int(ad_feedback.text) > 1629134400:
            display_error("检测到作弊判定, 请尝试重新运行")
            break
            # todo: 延时, 重试
        elif int(ad_feedback.text) >= 6:  # 已点击6次, 停止
            break
        else:
            continue

    getcre_response = requests.post(work_url, data="act=getcre", headers=headers)

    if "您已经成功领取了奖励天使币" in getcre_response.text:
        display_info("打工成功")
    elif "作弊" in getcre_response.text:
        display_error("作弊判定, 打工失败, 重试...")
        # todo: 增加重试逻辑
    elif "请先登录再进行点击任务" in getcre_response.text:
        display_error("打工失败, cookie失效...")
    elif "服务器负荷较重" in getcre_response.text:
        display_error("打工失败, TSDM:\"服务器负荷较重，操作超时\"...")
    else:
        display_error("======未知原因打工失败, 已保存response=======")
        write_error("打工", getcre_response.text)

    return


def work_multi_post():
    cookies = get_cookies_by_domain(tsdm_domain)

    for user in cookies.keys():
        display_info("正在打工: %s" % user)
        try:
            work_single_post(cookies[user])
        except Exception as e:
            display_error("====post打工出错: %s=====" % e)

    display_info("POST方式: 全部打工完成")
    return


def sign_single_post_v2(cookie):
    cookie_serialized = get_serialized_cookie(cookie)

    # 必须要这个content-type, 否则没法接收
    headers = HEADER_TSDM_SIGN
    headers['cookie_list'] = cookie_serialized

    s = requests.session()
    sign_response = s.get(tsdm_sign_url, headers=headers).text

    form_start = sign_response.find("formhash=") + 9  # 此处9个字符
    formhash = sign_response[form_start:form_start + 8]  # formhash 8位

    sign_data = "formhash=" + formhash + "&qdxq=wl&qdmode=3&todaysay=&fastreply=1"  # formhash, 签到心情, 签到模式(不发言)

    sign_response = s.post(sign_url_with_param, data=sign_data, headers=headers)

    if "恭喜你签到成功!获得随机奖励" in sign_response.text:
        display_info("签到成功")
    elif "您今日已经签到" in sign_response.text:
        display_info("该账户已经签到过")
    elif "已经过了签到时间段" in sign_response.text or "签到时间还没有到" in sign_response.text:
        display_error("签到失败: 目前不在签到时间段")
    elif "未定义操作" in sign_response.text:
        display_error("%s签到失败, 可能是formhash获取错误" % datetime.now())
        write_error("签到", sign_response.text)
    else:
        display_error("%s======未知原因签到失败, 已保存response=======" % datetime.now())
        write_error("签到", sign_response.text)

    return


def sign_multi_post():
    cookies = get_cookies_by_domain(tsdm_domain)

    for user in cookies.keys():
        display_info("%s正在签到: %s" % (datetime.now(), user))
        try:
            sign_single_post_v2(cookies[user])
        except Exception as e:
            display_error("%s====post签到出错: %s===" % (datetime.now(), e))

        time.sleep(random.uniform(0.5, 1))

    display_info("POST方式: 全部签到完成")
    return
