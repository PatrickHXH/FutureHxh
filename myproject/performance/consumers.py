import json
import time
import psutil
import httpx
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import datetime
from threading import Lock
import math
import psutil
import paramiko
from myproject.settings import BASE_DIR
import os
# print(BASE_DIR)
# PKEY_PATH = os.path.join(BASE_DIR,'performance','pkey.txt')

class CPUConsumer(WebsocketConsumer):

    # websocket建立连接时执行方法
    def connect(self):
        global cpu_thread
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.group_name = f'cpu_used'
        print("当前频道组：", self.group_name)
        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # private_key = paramiko.RSAKey.from_private_key_file(PKEY_PATH)
        # ssh.connect(hostname="121.4.54.4",port=22,username="root",pkey=private_key)
        # stdin, stdout, stderr = ssh.exec_command('top')
        print("打印看看是啥：",stdin, stdout, stderr)
        print(stdout.read())

        # 接受所有websocket请求
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        print("断开连接")
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("cpu 接收 message", message)

        # 发送消息到频道组，频道组调用cpu_background_thread方法
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'cpu_background_thread',
                'message': message
            }
        )

    def cpu_background_thread(self, event):
        message = event['message']
        print("cpu msg 开始", message)
        count = 0
        for i in range(10):
            count += 1
            time.sleep(2)
            t = time.strftime('%H:%M:%S', time.localtime())
            cpu = psutil.cpu_percent(interval=None, percpu=True)
            text = json.dumps({"message": {"data": [t, cpu], "count": count}})
            print("cpu-->", text)
            self.send(text_data=text)

class MemoryConsumer(WebsocketConsumer):

    # websocket建立连接时执行方法
    def connect(self):
        global cpu_thread
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.group_name = f'memory_used'

        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        # 接受所有websocket请求
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        print("断开连接")
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("memory 接收 message", message)

        # 发送消息到频道组，频道组调用memory_background_thread方法
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'memory_background_thread',
                'message': message
            }
        )

    def memory_background_thread(self, event):
        message = event['message']
        print("memory msg 开始", message)
        count = 0
        for i in range(10):
            count += 1
            time.sleep(2)
            t = time.strftime('%H:%M:%S', time.localtime())
            memory = psutil.virtual_memory()
            print("memory-->", t, type(memory), memory)
            used_mem = math.ceil(memory.used / (1024 * 1024))
            percent_mem = memory.percent
            print("t", t)
            print("used_mem", used_mem)
            print("count", count)
            print("percent_mem", percent_mem)
            text = json.dumps({"message": {"data": [str(t), str(used_mem)], "count": str(count), "percent": str(percent_mem)}})
            self.send(text_data=text)
