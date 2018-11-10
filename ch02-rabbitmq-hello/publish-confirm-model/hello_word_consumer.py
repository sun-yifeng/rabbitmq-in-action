# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2018/11/10 2:18 PM
# @Author: sunyf
# @File  : hello_word_consumer.py

import pika

# 用户认证信息
credentials = pika.PlainCredentials("guest", "guest")
# 连接代理服务
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)
# 获取代理服务
conn_broker = pika.BlockingConnection(conn_params)
# 获取通信信道
channel = conn_broker.channel()

# 声明交换器（如果已经创建则忽略）
channel.exchange_declare(exchange="hello-exchange",
                         exchange_type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False
                         )
""" 以上代码，生产者消费者相同 """

# 声明队列
channel.queue_declare(queue="hello-queue")

# 绑定队列和交换器（hola是路由键）
channel.queue_bind(queue="hello-queue",
                   exchange="hello-exchange",
                   routing_key="hola"
                   )
# 处理收到的消息
def msg_consumer(channel, method, header, body):
    # 发送投递模式：确认收到消息
    channel.basic_ack(delivery_tag=method.delivery_tag)
    # 如果发送的消息为quit则退出
    if body == 'quit':
        # 结束消费，关闭信道和连接
        channel.basic_cancle(consumer_tag="hello-consumer")
        channel.stop_consuming()
    else:
        print body
    return

# 订阅消息
channel.basic_consume(msg_consumer,
                      queue="hello-queue",
                      consumer_tag="hello-consumer"
                      )

# 等待消息进入（阻塞的方法）
channel.start_consuming()