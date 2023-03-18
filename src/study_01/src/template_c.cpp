#include "ros/ros.h"

int main(int argc, char *argv[])
{
    //执行节点初始化
    ros::init(argc, argv, "hello_c");
    
    //输出日志
    ROS_INFO("haha");

    return 0;
}
