
#!/usr/bin/env python
import math
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

pose = 0.0

class laserread:
        
        def __init__(self):
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
                self.rightInd = 0
                self.leftInd = 0
                self.left45 = 0
                self.right45 = 0
                self.avgRt = 0.0
                self.avgLt = 0.0
                self.forwardScan = []
                self.data = []
                self.ranges = []
                #rospy.init_node("Laser_listerner", anonymous=False)
                rospy.Subscriber("/robot0/laser_0", LaserScan, self.callback)

        def scanResults(self):
           #print "Forward scan has been called"
           #print self.rightInd
           #print self.leftInd
           for x in range(self.rightInd, self.leftInd):
               #print self.data.ranges[x]
               if self.data.ranges[x] < .3:  
                 return True
           return False
        
        def wallLeft(self):
            x1 = self.ranges[self.left45]
            x2 = self.ranges[leftInd]
            avgLt = (x1 + x2) / 2
        
        def wallRight(self:
            x1 = self.ranges[self.right45]
            x2 = self.ranges[rightInd]
            avgRt = (x1 + x2) / 2

        def callback(self, data):
           #print "LaserRead class, callback() function being called"

           for x in range(0,len(data.ranges)):
             self.ranges.append(0)
             self.ranges[x] = data.ranges[x]
             if math.isinf(data.ranges[x]):
               self.ranges[x] = data.range_max
           self.data = data         
           self.forwardIndex = int(len(data.ranges)/2)
           self.maxRan = data.range_max
           self.currentRange = self.ranges[self.forwardIndex]
           self.angleIncrement = data.angle_increment
           self.rightInd = int(((((-90 * 3.14) / 180) - data.angle_min) / data.angle_increment))
           self.leftInd = int(((((90 * 3.14) / 180) - data.angle_min) / data.angle_increment))
           self.right45 = int(((((-45 * 3.14) / 180) - data.angle_min) / data.angle_increment))
           self.left45 = int(((((45 * 3.14) / 180) - data.angle_min) / data.angle_increment))
           self.halfCount = self.counter/2
           self.desiredIndex = self.point - self.halfCount
           for i in range(0, len(data.ranges)):
	       if data.ranges[i] == data.range_max:
                  point = i
                  counter = counter + 1
               #elif data.ranges[i] < data.range_max:
                   #if counter > counter2:
                      #counter2 = counter
                      #point2 = point
                      #counter = 0
                #else:
                 #pass
            
def odomcallback(odom_data):
    #start callback for the odometer
    global pose 
    pose = odom_data.pose.pose.position.x
    #print "The odometer is at x = " + str(odom_data.pose.pose.position.x)

def go_forward():
        global pose
        stop = False
        t = False
	pub = rospy.Publisher("/robot0/cmd_vel", Twist, queue_size = 10)
        rospy.Subscriber("/robot0/odom", Odometry, odomcallback)
        myL = laserread()
	rospy.init_node("Controller", anonymous=True)
	rate = rospy.Rate(10)
        twistCmd = Twist();
	while not rospy.is_shutdown():
           while t == False:
              twistCmd.linear.x = myL.currentRange / myL.maxRan
              twistCmd.angular.z = 0
              pub.publish(twistCmd)
              rate.sleep()
              t = myL.scanResults()

           twistCmd.linear.x = 0
           twistCmd.angular.z = 0
           pub.publish(twistCmd)
           rate.sleep()

           while t == True:
              turn = myL.desiredIndex - myL.forwardIndex
              twistCmd.linear.x = 0
              twistCmd.angular.z = turn * myL.angleIncrement
              pub.publish(twistCmd)
              rate.sleep()
              t = myL.scanResults()



if __name__ == '__main__':
	try:
		go_forward()
	except rospy.ROSInterruptException:
		pass
