"""Import from redis to postgresql"""
import sys
sys.path.append('./')
from db.redisdb import RedisActionsLogModule

from bot.parser import CommParser
import time


def main():
    while True:
        tnum = 0.5
        logs = RedisActionsLogModule.get_query()
        if logs:
            tnum = 0.001
            CommParser(logs).actions_parser()
        time.sleep(tnum)

if __name__ == '__main__':
    main()