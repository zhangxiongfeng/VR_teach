# -*- coding: UTF-8 -*-
import sys
import socket
import threading
import websocket

SERVER_URL = "ws://dev-accwssail.healthmall.cn/server/bodyAnaylzer/data"
def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    #发送机器唯一标识码
    ws.send("{\"message\":\"register\",\"deviceID\":\"AR000001\"}")
   

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(SERVER_URL,

    on_message = on_message,
    on_error = on_error,
    on_close = on_close

    )
    ws.on_open = on_open
    ws.run_forever()
