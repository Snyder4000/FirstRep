#include "ros/ros.h"
#include "std_msgs/String.h"
#include "geometry_msgs/Twist.h"
#include "nav_msgs/Odometry.h"
#include "sensor_msgs/LaserScan.h"
#include <sstream>

ros::NodeHandle n;

void odomCallback()
{
  
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "controller");
  ros::Publisher chatter_pub = n.advertise<geometry_msgs::Twist>("twist", 1000);
  

  ros::Rate loop_rate(10);
  while (ros::ok())
  {
     geometry_msgs::Twist msg;
     msg.data.linear.x = .5;
     msg.data.angular.z = 0;
  }
  ros::spin();
  return 0;
}

class scannerLaser()
{
  public:
  float maxRan = 8.0;
  float currentRange = 1.0;
  int forwardIndex = 333;
  int counter = 0;
  int point = 0;
  int halfCount = counter/2;
  int desiredIndex = point - halfCount;
  float angleIncrement = 0;
  float angleMin = 0;
  int point2 = 0;
  int counter2 = 0;
  int rightInd = 0;
  int leftInd = 0;
  float forwardScan[];
  ros::Subscriber sub = n.subscribe("/robot0/laser_0", 1000, laserCallback);
  void laserCallback(sensor_msgs::LaserScan::ConstPtr& msg)
  {
    forwardScan = msg.data.ranges;
    forwardIndex = int(msg.data.ranges.size()/2);
    maxRan = msg.data.range_max;
    angleIncrement = msg.data.angle_increment;
    angleMin = msg.data.angle_min;
    rightInd = int(((((-90 * 3.14) / 180) - angleMin) / angleIncrement));
    leftInd = int(((((90 * 3.14) / 180) - angleMin) / angleIncrement));
  }
}
