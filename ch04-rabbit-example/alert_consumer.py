# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2018/11/11 1:52 PM
# @Author: sunyf
# @File  : alert_consumer.py.py

import json, smtplib
import pika, sys

# sys.path.append("/Library/Python/2.7/site-packages")
# print (sys.path)

def send_mail(recipients, subject, message):
    """ E-mail generator for received alert. """
    headers = ("From: %s\r\nTo: \r\n" + "Subject: %s\r\n\r\n") % ("9339996@qq.com", subject)
    # 定义邮箱服务器
    smtp_server = smtplib.SMTP()
    smtp_server.connect("mail.sunyf.com",25)
    smtp_server.sendmail("9339996@qq.com",
                         recipients,
                         headers + str(message)
                         )
    smtp_server.close()

# 通知处理程序（严重级别）
def critical_notify(channel, method, header, boby):
    """ Sends CRITICAL alerts to administrators via e-mail. """
    EMAIL_RECIPS = ["9339996@qq.com",]

    message = json.load(boby)

    # 将邮件传输到邮件服务器
    send_mail(EMAIL_RECIPS, "CRITICAL ALERT", message)

    print ("Send alert via e-mail! Alert Text: %s " + \
           "Recipients: %s") (str(message), str(EMAIL_RECIPS))

    # 发送投递确认
    channel.baic_ack(delivery_tag=method.delivery_tay)

# 通知处理程序（特殊级别）
def rate_limit_notify(channel, method, header, body):
    """ Sends the message to the administrator via e-mail. """
    EMAIL_RECIPS = ["sun_yifeng@aliyun.com",]

    # 将JSON消息解码
    message = json.load(body)

    send_mail(EMAIL_RECIPS, "RATE LIMIT ALERT!", message)

    print ("Sent alert via-mail! Alert Text: %s " + \
           "Recipients: %s") (str(message), str(EMAIL_RECIPS))

    #发送投递确认
    channel.baic_ack(deliviry_tag=method.delivery_tay)

# 告诉程序的主题位置
if __name__ == "__name__":
    # 代理参数设置
    AMQP_SERVER = "localhost"
    AMQP_USER = "alert_user"
    AMQP_PASS = "alertme"
    AMQP_VHOST = "/"
    AMQP_EXCHAGE = "alerts"

    # 建立到代理的连接
    creds_broker = pika.PlainCredentials(AMQP_USER, AMQP_PASS)

    conn_param = pika.ConnectionParameters(AMQP_SERVER,
                                           virtual_host=AMQP_VHOST,
                                           credentials=creds_broker,
                                           )

    conn_broker = pika.BlockingConnection(conn_param)

    channel = conn_broker()

    # 声明交换机
    channel.exchange_declare(exchange=AMQP_EXCHAGE,
                             exchange_type="topic",
                             auto_delete=False
                             )

    # 声明critical队列（严重级别）
    channel.queue_declare(queue="critical", auto_delete=False)
    # 队列绑定topic交换器（严重级别）
    channel.queue_bind(queue="critical",
                       exchange="alerts",
                       routing_key="critical.*"
                       )

    # 声明rate_limit队列（特殊级别）
    channel.queue_declare(queue="rate_limit", auto_delete=False)
    # 队列绑定topic交换器（特殊级别）
    channel.queue_bind(queue="rate_limit",
                       exchange="alerts",
                       routing_key="*.rate_limit"
                       )

    # 设置报警处理程序（严重级别）
    channel.basic_consume(critical_notify,
                          queue="critical_notify",
                          no_ack=False,
                          consumer_tag="critical"
                          )

    # 设置报警处理程序（特殊级别）
    channel.basic_consume(rate_limit_notify,
                          queue="rate_limit",
                          no_ack=False,
                          consumer_tag="rate_limit"
                          )

    print "Ready for alerts!"

    # 启动消费者监听程序
    channel.basic_consuming()










