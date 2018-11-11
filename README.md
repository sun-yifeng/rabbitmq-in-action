# rabbitmq-in-action

1、启动mq代理服务器（应用程序和节点同时启动）
$MQ_HOME/sbin/rabbitmq-server

2、查看服务器的状态
$MQ_HOME/sbin/rabbitmqctl status

3、停止mq代理服务器（应用程序和节点同时关闭）
$MQ_HOME/sbin/rabbitmqctl stop

4、登录
http://localhost:15672
guest/guest

5、权限控制
./rabbitmqctl list_users                       查看用户
./rabbitmqctl add_user cashing-tier cashMe1    创建用户
./rabbitmqctl list_vhosts                      查看vhost
./rabbitmqctl add_vhost oak                    创建vhost

./rabbitmqctl list_permissions -p oak                                      查看权限
./rabbitmqctl set_permissions -p oak cashing-tier ".*" ".*" ".*"           创建权限
./rabbitmqctl clear_permissions -p oak cashing-tier                        创建权限

6、统计信息
./rabbitmqctl list_queues                      查看队列和消息数
./rabbitmqctl list_exchanges                   查看交换器和绑定
./rabbitmqctl list_bindings                    查看绑定信息


