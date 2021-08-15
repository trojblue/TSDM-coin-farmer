from actions import *
from v2_request import *
from datetime import datetime
import schedule
import json

def do_print():
    print(time.time())



def change_format():
    c = read_cookies()
    c_json = json.dumps(c, ensure_ascii=False)

    print("D")


if __name__ == '__main__':
    # update_new_accounts()
    # refresh_all_cookies(TSDM_credentials)
    # work_multiple

    # sign_multiple()
    # print(datetime.now())
    # schedule.every(3).seconds.do(do_print)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep

    # change_format
    # all_cookies = list(read_cookies().values())
    work_multi_post()
    # refresh_all_cookies
    # c = read_cookies()
    # print("D")




