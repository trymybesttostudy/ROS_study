#! /usr/bin/env python
#-*- coding: UTF-8 -*- 

import rospy # 1.导包

from std_msgs.msg import Float64

def velocity_publisher():
# ROS节点初始化
    rospy.init_node('velocity_publisher', anonymous=True)

# 创建一个Publisher，发布名为/turtle1/cmd_vel的topic，消息类型为geometry_msgs::Twist，队列长度10
    # 右前腿
    turtle1_vel_pub = rospy.Publisher('/toydog/joint1_position_controller/command', Float64, queue_size=10)
    turtle2_vel_pub = rospy.Publisher('/toydog/joint2_position_controller/command', Float64, queue_size=10)
    # 左前腿
    turtle3_vel_pub = rospy.Publisher('/toydog/joint3_position_controller/command', Float64, queue_size=10)
    turtle4_vel_pub = rospy.Publisher('/toydog/joint4_position_controller/command', Float64, queue_size=10)
    # 右后腿
    turtle5_vel_pub = rospy.Publisher('/toydog/joint5_position_controller/command', Float64, queue_size=10)
    turtle6_vel_pub = rospy.Publisher('/toydog/joint6_position_controller/command', Float64, queue_size=10)
    # 左后腿
    turtle7_vel_pub = rospy.Publisher('/toydog/joint7_position_controller/command', Float64, queue_size=10)
    turtle8_vel_pub = rospy.Publisher('/toydog/joint8_position_controller/command', Float64, queue_size=10)

#设置循环的频率
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
# 初始化geometry_msgs::Twist类型的消息
        vel_msg1 = Float64()
        vel_msg1.data = -1
        vel_msg2 = Float64()
        vel_msg2.data = 1
        vel_msg3 = Float64()
        vel_msg3.data = -1
        vel_msg4 = Float64()
        vel_msg4.data = 1

# 发布消息
        turtle1_vel_pub.publish(vel_msg1)
        rospy.loginfo("Publsh turtle velocity command[%0.2f]", vel_msg1.data)
        turtle2_vel_pub.publish(vel_msg1)
        rospy.loginfo("Publsh turtle velocity command[%0.2f]", vel_msg1.data)
        turtle3_vel_pub.publish(vel_msg2)
        rospy.loginfo("Publsh turtle velocity command[%0.2f]", vel_msg2.data)
        turtle4_vel_pub.publish(vel_msg2)
        rospy.loginfo("Publsh turtle velocity command[%0.2f]", vel_msg2.data)
        turtle5_vel_pub.publish(vel_msg3)
        rospy.loginfo("Publsh turtle velocity command[%0.2f]", vel_msg3.data)
        turtle6_vel_pub.publish(vel_msg3)
        rospy.loginfo("Publsh turtle velocity command[%0.2f]", vel_msg3.data)
        turtle7_vel_pub.publish(vel_msg4)
        rospy.loginfo("Publsh turtle velocity command[%0.2f]", vel_msg4.data)
        turtle8_vel_pub.publish(vel_msg4)
        rospy.loginfo("Publsh turtle velocity command[%0.2f]", vel_msg4.data)

# 按照循环频率延时
        rate.sleep()

if __name__ == '__main__':
    try:

        rospy.loginfo("Hello VScode, 我是 Python ....")  #3.日志输出 HelloWorld
        velocity_publisher()
    except rospy.ROSInterruptException:
        pass