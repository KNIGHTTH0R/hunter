"""Import from redis to postgresql"""
import sys

sys.path.append('./')
from db.redisdb import RedisLogModule

from bot.parser import CommParser
import time


def main():
    while True:
        tnum = 0.5
        logs = RedisLogModule.get_query()
        if logs:
            tnum = 0.01

            CommParser(logs).achive_parser()
            try:
                CommParser(logs).subscribe()
            except:
                pass
        time.sleep(tnum)

if __name__ == '__main__':
    main()