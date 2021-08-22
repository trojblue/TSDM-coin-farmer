import argparse
import time, sys, schedule

from v1_selenium import *
from v2_request import *
from credentials import TSDM_credentials
from dlc_stage1st import do_read_s1


def heartbeat():
    print("heartbeat: ", datetime.now())


def do_parse():
    parser = argparse.ArgumentParser()
    action_group = parser.add_mutually_exclusive_group()

    action_group.add_argument("-s", "--selenium", help="运行: 使用selenium模式(不填默认用post模式)", action="store_true")
    action_group.add_argument("-r", "--reset", help="刷新cookie", action="store_true")

    parser.add_argument("-n", "--now", help="立刻运行打工和签到", action="store_true")

    args = parser.parse_args()

    if args.reset:
        print("刷新cookie")
        refresh_all_cookies(TSDM_credentials)
        print("所有cookie刷新完毕")
        sys.exit()

    elif args.selenium:
        print("使用selenium模式运行")
        schedule.every(362).minutes.do(work_multi_selenium)
        schedule.every().day.at("10:30").do(sign_multi_selenium)    # 每天 10:30 签到

    else:
        print("默认: 使用post模式运行")
        schedule.every(362).minutes.do(work_multi_post)
        schedule.every().day.at("10:30").do(sign_multi_post)

    if args.now:
        print("[-n] 立即进行:")
        if args.reset:
            print("刷新cookie时-n选项无效")
            pass
        elif args.selenium:
            work_multi_selenium()
            sign_multi_selenium()
        else:
            work_multi_post()
            sign_multi_post()

    # 需要s1功能的话取消下面的注释
    # schedule.every(20).minutes.do(do_read_s1)

def do_schedule():
    print("正在运行计划任务, 每6小时签到一次")

    while True:
        print("距离下一次任务的时间: {:.1f}分钟".format(schedule.idle_seconds()/60), end='\r')
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(10)


if __name__ == '__main__':
    do_parse()
    do_schedule()
