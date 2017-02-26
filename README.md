Ingress Bot

Requirements:
python2.7 (get cookies)
python3.5
postgresql95
redis
mitmproxy (for proxy parse)

Source has more legacy code. 

Installing:
1. "virtualenv --python=3.5 venv"
". venv/bin/activate"
"pip install -r requirements.txt"
"Use "virtualenv --python=3.5 venv2" for cookies"
2. Migrate DB scheme (utils/schema.sql).
3. Add accounts to table cookies
4. Add map area for scanning to table tasks
5. Add supervisor config or just run tools/(get_log, logger_achive, logger_player, get_cookies)

Demo:
https://ingress-guard.tk
