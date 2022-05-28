from lib.v1_selenium import *
from lib.v2_request import *
from lib.logger import *
from private.settings import EAT_CREDENTIALS

eat_login_url = "https://eatasmr.com/community"
eat_attendance_url = "https://eatasmr.com/tasks/attendance"
eat_sign_url_without_formhash = "https://eatasmr.com/tasks/attendance?a=check&__v="


def refresh_cookies_eatasmr():
    """从credentials重新获取所有cookie
    """
    cred = EAT_CREDENTIALS[0]
    refresh_cookie_eatasmr(cred[0])
    return


def refresh_cookie_eatasmr(username: str):
    """selenium获取cookie
    """
    add_debug("刷新cookie")
    driver = get_webdriver()
    driver.get(eat_login_url)
    driver.find_element_by_xpath("//*[@id=\"menu-item-13336\"]/a").click()

    done = input("登录完成后按回车: ")



    my_username = username
    new_cookie = driver.get_cookies()
    driver.close()

    write_new_cookie_all(new_cookie, my_username)
    return new_cookie

def do_sign_eat_single(cookie:List):
    """浏览一个帖子
    """
    headers = get_headers(cookie, HEADER_EAT_SIGN)
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
    display_info("正在eatASMR签到...")

    for user in eat.keys():
        display_info("%s eatASMR签到: %s"%(datetime.now(), user))
        do_sign_eat_single(eat[user])

    display_info("eatASMR签到完成")

if __name__ == '__main__':
    do_read_eat_all()
    # refresh_cookies_eatasmr()