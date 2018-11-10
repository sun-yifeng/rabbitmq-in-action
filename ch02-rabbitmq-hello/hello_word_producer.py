# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2018/11/10 2:18 PM
# @Author: sunyf
# @File  : hello_word_producer.py

import pika, sys

# 用户认证信息
credentials = pika.PlainCredentials("guest", "guest")
# 连接代理服务
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)
# 获取代理服务
conn_broker = pika.BlockingConnection(conn_params)
# 获取通信信道
channel = conn_broker.channel()

# 声明交换器
channel.exchange_declare(exchange="hello-exchange",
                         exchange_type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False
                         )
""" 以上代码，生产者消费者相同 """

# 定义消息，注意：argv[1]为hello word或者quit
msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

# 发布消息
channel.basic_publish(body=msg,
                      exchange="hello-exchange",
                      properties=msg_props,
                      routing_key="hola"
                      )

