#include "ros/ros.h"

int main(int argc, char *argv[])
{
    //解决乱码问题
    setlocale(LC_ALL,"");

    //执行节点初始化
    ros::init(argc, argv, "hello_c");
    
    //输出日志
    ROS_INFO("haha,哈哈哈");

    return 0;
}
