"""Import from redis to postgresql"""
import sys
sys.path.append('./')
from db.redisdb import PlayerLogModule

from bot.parser import CommParser
import time


def main():
    while True:
        tnum = 1800
        logs = PlayerLogModule.get_query()
        if logs:
            CommParser(logs).player_parser()
        time.sleep(tnum)

if __name__ == '__main__':
    main()
