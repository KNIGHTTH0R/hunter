#!/bin/bash

pyinstaller tools/get_log.py -F
pyinstaller tools/logger_achive.py -F
pyinstaller tools/logger_player.py -F

docker build . -t ingressguard/main