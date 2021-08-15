from cookie import *

"""
selenium方式的签到/打工
"""


def sign_single(cookies):
    """签到主程序
    """
    driver = webdriver.Chrome()

    driver.get(sign_page)  # selenium: 必须先访问一次来获取cookie domain
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get(sign_page)  # 回到签到页
    print("返回签到页....")
    time.sleep(0.5)

    try:
        silent_btn = driver.find_elements_by_name("qdmode")[1]
    except Exception:
        print("未找到按钮, 可能已经签过到")
        driver.quit()
        return

    # 没签过到
    silent_btn.click()  # 不填写签到留言
    time.sleep(0.5)

    driver.find_element_by_id('kx').click()  # 签到心情: 开心
    pages = driver.window_handles
    driver.switch_to.window(pages[0])
    time.sleep(0.5)

    driver.find_element_by_xpath('//*[@id="qiandao"]/table[1]/tbody/tr/td/div/a[1]').click()  # 提交
    # 如果失效了这样更新: https://stackoverflow.com/questions/39864280/xpath-for-elements-using-chrome

    # TODO: 添加签到成功验证
    print("签到完成")
    return


def work_single_click(driver, eleement):
    """点击单个广告, 然后返回签到页
    """
    # driver.find_element_by_id(element_id).click()
    eleement.click()
    time.sleep(0.2)
    og, popup = driver.window_handles[0], driver.window_handles[1]
    driver.switch_to.window(popup)
    driver.close()
    driver.switch_to.window(og)


def work_single(cookies):
    """打工主程序
    """
    driver = webdriver.Chrome()

    driver.get(work_page)  # selenium: 必须先访问一次来获取cookie domain
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get(work_page)  # 回到打工页
    time.sleep(0.5)

    try:
        driver.find_element_by_id("np_advid1")
    except Exception:
        print("未找到按钮, 可能已经打工过")
        driver.quit()
        return

    for i in driver.find_elements_by_xpath("//*[starts-with(@id,'np_advid')]"):
        work_single_click(driver, i)

    driver.find_element_by_xpath('//*[@id="stopad"]/a').click()  # TODO: 容易失效, 更新成post
    time.sleep(2)

    print("打工完成")
    driver.quit()

    return  # TODO: 添加成功与否查询


def sign_multiple():
    all_cookies = read_cookies()
    for account in all_cookies.keys():
        print("正在签到账号: ", account)
        sign_single(all_cookies[account])

    print("全部账号签到完成")


def work_multiple():
    all_cookies = read_cookies()
    for account in all_cookies.keys():
        print("正在打工账号: ", account)
        work_single(all_cookies[account])

    print("全部账号打工完成")
