from ib_insync import IB, util


util.logToConsole(True)  # see handshake messages while debugging
ib = IB()
ib.connect(host='172.21.224.1', port=7497, clientId=205, timeout=10)
print('Connected:', ib.isConnected())