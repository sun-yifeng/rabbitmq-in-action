# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2018/11/10 2:18 PM
# @Author: sunyf
# @File  : hello_word_producer.py

import pika, sys
from pika import spec

# 用户认证信息
credentials = pika.PlainCredentials("guest", "guest")
# 连接代理服务
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)
# 获取代理服务
conn_broker = pika.BlockingConnection(conn_params)

# 获取通信信道
channel = conn_broker.channel()

""" 发送确认模式 """

# 在BlockingConnection中，basic_publish实现了书中confirm_handler这个函数
# 回调函数：发送发确认时调用
# def confirm_handler(frame):
#     if type(frame.method) == spec.Confirm.SelectOk:
#         print "Channel in 'confirm' mode. "
#     elif type(frame.method) == spec.Basic.Nack:
#         if frame.method.delivery_tay in msg_ids:
#             print "Message lost!"
#     elif type(frame.method) == spec.Basic.Ack:
#         if frame.method.delivery_tay in msg_ids:
#             print "Confirm received!"
#             msg_ids.remove(frame.method.delivery_tay)

# 设置为确认模式（非事务模式）
# channel.confirm_delivery(callback=confirm_handler)
channel.confirm_delivery()

# 定义消息,注意：argv[1]为运行时的参数,如hello,quit
msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
# 定义消息ID追踪器
msg_ids = []

# 发布消息
ack = channel.basic_publish(body=msg,
                            exchange="hello-exchange",
                            properties=msg_props,
                            routing_key="hola"
                      )
if ack == True:
    print "put message to rabbitmq successful!!!"
else:
    print "put message to rabbitmq failed!!!"

# ID追加到列表中7
msg_ids.append(len(msg_ids) + 1)
channel.close()

