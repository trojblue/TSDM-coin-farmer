from farmer import *

def get_multiple_cookie(credentials):
    """从credentials获取所有cookie
    用之前记得删掉原有的cookies.pickle
    """
    for i in credentials:
        get_cookie(i[0], i[1])
    return


def update_new_accounts():
    """根据TSDM_credentials,
    添加新的cookie, 但是不刷新老账户
    """
    usernames = read_cookies().keys()
    new_cred = []

    for cred in TSDM_credentials:
        if cred[0] not in usernames:
            new_cred.append(cred)

    print("添加", len(new_cred), "个新账户:")
    get_multiple_cookie(new_cred)
    return


def work_multiple():
    all_cookies = read_cookies()
    for account in all_cookies.keys():
        print("正在打工账号: ", account)
        work_single(all_cookies[account])

    print("全部账号打工完成")

def sign_multiple():
    all_cookies = read_cookies()
    for account in all_cookies.keys():
        print("正在签到账号: ", account)
        sign_single(all_cookies[account])

    print("全部账号签到完成")


if __name__ == '__main__':
    # update_new_accounts()
    # get_multiple_cookie(TSDM_credentials)
    work_multiple()




