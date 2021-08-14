from utils import *
from credentials import TSDM_credentials
from farmer import *



def get_multiple_cookie():
    """从credentials获取所有cookie
    用之前记得删掉原有的cookies.pickle
    """
    for i in TSDM_credentials:
        get_cookie(i[0], i[1])
    return


def work_multiple():
    all_cookies = read_cookies()
    for account in all_cookies.keys():
        print("正在打工账号: ", account)
        work_single(all_cookies[account])

    print("全部账号打工完成")


if __name__ == '__main__':
    # get_multiple_cookie()
    work_multiple()


    print("D")
    # get_dir()
    # c = read_cookies()

