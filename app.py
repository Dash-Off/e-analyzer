import os
from eanalyze import EAnalyze
from dashoff_util import DashOffUtil
def add(a, b):
    return a+b

def getResult(dashOffId, raw):
    payload = EAnalyze(text=raw).get_result_payload()
    DashOffUtil.update_result(dashOffId, payload)
    return payload

from server import RPCServer
port = int(os.environ.get("PORT", 8080))
print(port)
server = RPCServer('0.0.0.0', port)

server.register_call(add)
server.register_call(getResult)

server.run()
