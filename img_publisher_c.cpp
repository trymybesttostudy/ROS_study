#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/highgui/highgui.hpp>
#include <std_msgs/String.h>
 
int main( int argc, char **argv )
{
  ros::init( argc, argv, "pub_opencv" );
  ros::NodeHandle n;
 
  // Open camera with CAMERA_INDEX (webcam is typically #0).
  const int CAMERA_INDEX = 1;
  cv::VideoCapture capture( CAMERA_INDEX ); //摄像头视频的读操作
  if( not capture.isOpened() )
  {
    ROS_ERROR_STREAM(
      "Failed to open camera with index " << CAMERA_INDEX << "!"
    );
    ros::shutdown();
  }
  //1 捕获视频
 
  //2 创建ROS中图像的发布者
  image_transport::ImageTransport it( n ); 
  image_transport::Publisher pub_image = it.advertise( "camera/image", 1 );
 
 
  //cv_bridge功能包提供了ROS图像和OpenCV图像转换的接口，建立了一座桥梁
  cv_bridge::CvImagePtr frame = boost::make_shared< cv_bridge::CvImage >();
  frame->encoding = sensor_msgs::image_encodings::BGR8;

  while( ros::ok() ) {
    capture >> frame->image; //流的转换
    if( frame->image.empty() )
    {
      ROS_ERROR_STREAM( "Failed to capture frame!" );
      ros::shutdown();
    }
    //打成ROS数据包
    frame->header.stamp = ros::Time::now();
    pub_image.publish( frame->toImageMsg() );
 
    cv::waitKey( 1000 );//opencv刷新图像 1s
    ros::spinOnce();
  }
 
  capture.release();  //释放流
  return EXIT_SUCCESS;
}