
def refresh_cookie_tsdm(username: str, password: str):
    """selenium获取cookie
    """
    add_debug("刷新cookie")
    driver = get_webdriver()
    driver.get(login_url)
    driver.find_element_by_xpath("//*[starts-with(@id,'cookietime_')]").click()

    if username and password: # 账户密码非空
        driver.find_element_by_xpath("//*[starts-with(@id,'username_')]").send_keys(username)
        driver.find_element_by_xpath("//*[starts-with(@id,'password3_')]").send_keys(password)
        driver.find_element_by_name("tsdm_verify").click()
        display_info("等待浏览器里填写验证码并登录:")
    else:
        # 无TSDM_CREDENTIAL, 手动填写信息
        display_warning("请手动填写信息后点击登录:")

    wait = WebDriverWait(driver, 100)
    wait.until(EC.title_contains("提示信息 - "))

    if not username:
        # 无TSDM_CREDENTIAL, 从浏览器获取用户名
        my_username = driver.find_element_by_xpath("//*[@id='um']/p[1]/strong/a").text
        assert my_username is not None
    else:
        my_username = username

    new_cookie = driver.get_cookies()
    driver.close()

    write_new_cookie(new_cookie, my_username)
    return new_cookie

def refresh_cookies_tsdm():
    """从credentials重新获取所有cookie
    """
    try:
        # 多账户刷新
        from settings import TSDM_CREDENTIALS
        for i in TSDM_CREDENTIALS:
            refresh_cookie_tsdm(i[0], i[1])

    except ImportError:
        display_warning("未找到TSDM_credentials, 为单个账户手动刷新cookie; \n"
              "如果需要多账户签到/自动填写密码, 请先按照readme设置好天使动漫的账户密码")
        refresh_cookie_tsdm("", "")

    return


def get_cookies_all(path:str) -> Dict:
    """从文件读取所有cookies
    { username: [cookie] }
    """
    try:
        with open(path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data

    except FileNotFoundError:  # 文件不存在
        display_warning("cookies.json不存在")
        return {}


def get_cookies_by_domain(domain:str):
    """从所有cookie里分离出指定域名的cookie
    domain: cookie domain, (".tsdm39.net")
    """
    cookies_all = get_cookies_all(COOKIE_PATH) #     { username: [cookie] }
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