
#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

pose = 0.0

class laserread:
        
        def __init__(self):
                self.FirstValue=0
                self.maxRan = 8.0
                self.currentRange = 1.0
                self.forwardIndex = 333
                self.counter = 0
                self.point = 0
                self.halfCount = self.counter/2
                self.desiredIndex = self.point - self.halfCount
                self.angleIncrement = 0
                self.point2 = 0
                self.counter2 = 0
                #rospy.init_node("Laser_listerner", anonymous=False)
                rospy.Subscriber("/robot0/laser_0", LaserScan, self.callback)

        def callback(self, data):
            #rospy.loginfo(rospy.get_caller_id() + "The First Value is " + str(data.ranges[FirstValue]))
            print "LaserRead class, callback() function being called"
            forwardIndex = int(len(data.ranges)/2)
            maxRan = data.range_max
            currentRange = data.ranges[forwardIndex]
            angleIncrement = data.angle_increment
            for i in range(0, len(data.ranges)):
		if data.ranges[i] == data.range_max:
                   point = i
                   counter = counter + 1
                elif data.ranges[i] < data.range_max:
                   if counter > counter2:
                      counter2 = counter
                      point2 = point
                      counter = 0
                else:
                 pass
            
def odomcallback(odom_data):
    #start callback for the odometer
    global pose 
    pose = odom_data.pose.pose.position.x
    #print "The odometer is at x = " + str(odom_data.pose.pose.position.x)

def go_forward():
        global pose
	pub = rospy.Publisher("/robot0/cmd_vel", Twist, queue_size = 10)
        rospy.Subscriber("/robot0/odom", Odometry, odomcallback)
        myL = laserread()
	rospy.init_node("Controller", anonymous=True)
	rate = rospy.Rate(10)
        twistCmd = Twist();
        print "Laser reader class variable maxRan is: " + str(myL.maxRan)
	while pose < 4:
                #print "globabl variable pose is: " + str(pose)
                
                twistCmd.linear.x = myL.currentRange / myL.maxRan
		twistCmd.angular.z = 0
		pub.publish(twistCmd)
		rate.sleep()

        twistCmd.linear.x = 0
        twistCmd.angular.z = 0
        pub.publish(twistCmd)
        rate.sleep()

        #while :
         #turn = myL.desiredIndex - myL.forwardIndex
         #twistCmd.linear.x = myL.currentRange / myL.maxRan
         #twistCmd.angular.z = turn * myL.angleIncrement
         #pub.publish(twistCmd)
         #rate.sleep()

        #twistCmd.linear.x = 0
        #twistCmd.angular.z = 0
        #pub.publish(twistCmd)
        #rate.sleep()

if __name__ == '__main__':
	try:
		go_forward()
	except rospy.ROSInterruptException:
		pass
