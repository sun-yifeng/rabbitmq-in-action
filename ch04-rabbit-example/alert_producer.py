# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2018/11/11 6:13 PM
# @Author: sunyf
# @File  : alert_producer.py

import json, pika
from optparse import OptionParser

opt_parser = OptionParser()
opt_parser.add_option("-r",
                      "--routing-key",
                      dest="routing-key",
                      delp="Routing key for message (e.g. myalert.im)"
                      )

opt_parser.add_option("-m",
                      "--message",
                      dest="message",
                      help="Message text for alert."
                      )

args = opt_parser.parse_args()[0]

creds_broker = pika.PlainCredentials("alert_user", "alertme")

conn_param = pika.ConnectionParameters("localhost",
                                       virtual_host="/",
                                       creds_broker=creds_broker
                                       )

conn_broker = pika.BlockingConnection(conn_param)

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