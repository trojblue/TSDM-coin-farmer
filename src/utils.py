from selenium import webdriver
import pickle
import time
import os

login_page = 'https://www.tsdm39.net/member.php?mod=logging&action=login'

USERNAME = '独看流云'
PASSWORD = ''
SAVE_PATH = '../bin'
FILENAME = 'cookies.pickle'

def get_cookie():
    """selenium获取cookie
    """
    browser = webdriver.Chrome()
    browser.get(login_page)

    browser.find_element_by_xpath("//*[starts-with(@id,'username_')]").send_keys(USERNAME)
    browser.find_element_by_xpath("//*[starts-with(@id,'password3_')]").send_keys(PASSWORD)

    man_verify_code = input("input verification：")

    browser.find_element_by_name("tsdm_verify").send_keys(man_verify_code)
    browser.find_element_by_name("loginsubmit").click()
    time.sleep(1)

    print("start dumping cookies")
    tsdm_cookies = browser.get_cookies()

    browser.quit()
    save_cookies(tsdm_cookies)
    return tsdm_cookies

def read_cookies():
    """从文件读取cookie
    """
    output_path = os.path.join(SAVE_PATH, FILENAME)
    f = open(output_path, 'rb')
    tsdm_cookies = pickle.load(f)
    f.close()

    return tsdm_cookies

def save_cookies(tsdm_cookies) -> None:
    """写入cookie到文件
    """
    directory = os.path.dirname(SAVE_PATH)
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_path = os.path.join(SAVE_PATH, FILENAME)
    f = open(output_path, 'wb')
    pickle.dump(tsdm_cookies, f)
    f.close()
    print("write done")


def load_cookies(driver) -> None:
    """获取cookie, 并且载入浏览器
    """
    directory = os.path.dirname(SAVE_PATH)
    if not os.path.exists(directory):
        print("文件夹不存在, 获取cookie...")
        cookies = get_cookie()
    else:
        print("读取cookie....")
        cookies = read_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    return
