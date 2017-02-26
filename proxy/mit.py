import json
import sys
sys.path.append('./')
from bot.parser import InventoryScannerParser


def response(flow):
    if flow.request.host == 'm-dot-betaspike.appspot.com':

        headers = []
        for i in flow.response.headers:
            headers.append(flow.response.headers[i])

        if 'application/json; charset=utf-8' in headers:
            # if flow.request.path == '/rpc/playerUndecorated/getInventory':
            #     print(json.loads(flow.response.content.decode('UTF-8')))
            InventoryScannerParser(flow.response.content, flow.request.path, flow.request.headers)
