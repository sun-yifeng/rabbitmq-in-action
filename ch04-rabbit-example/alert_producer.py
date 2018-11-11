# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2018/11/11 6:13 PM
# @Author: sunyf
# @File  : alert_producer.py

import json, pika
from optparse import OptionParser

# 读取命令行
opt_parser = OptionParser()
# 路邮键
opt_parser.add_option("-r",
                      "--routing-key",
                      dest="routing-key",
                      help="Routing key for message (e.g. myalert.im)"
                      )
# 消息告警
opt_parser.add_option("-m",
                      "--message",
                      dest="message",
                      help="Message text for alert."
                      )

args = opt_parser.parse_args()[0]

# 建立到服务器的连接
creds_broker = pika.PlainCredentials("alert_user", "alertme")

# 连接参数设置
conn_params = pika.ConnectionParameters("localhost",
                                       virtual_host="/",
                                       credentials=creds_broker
                                       )
# 消息代理服务器
conn_broker = pika.BlockingConnection(conn_params)

# 获取通信信道
channel = conn_broker.channel()

msg = json.dump(args.message)
msg_props = pika.BasicProperties()
msg_props.content_type = "application/json"
msg_props.durable = False

# 发布消息（告警信息）
channel.basic_publish(body=msg,
                      exchange="alert",
                      properties=msg_props,
                      routing_key=args.routing_key
                      )

print ("Sent message %s tagged with routing key '%s' to  exchange '/'. ") % (json.dumps(args.message),
                                                                             args.routing_key
                                                                             )