#!/usr/bin/env python

import roslib; roslib.load_manifest('nxt_ros')
import nxt.locator
import rospy
import math
from nxt.motor import PORT_A
from nxt.sensor import PORT_1, PORT_2
from nxt.sensor import Type
import nxt.sensor
import nxt.motor
from sensor_msgs.msg import JointState
from nxt_msgs.msg import Contact, JointCommand

class nxtController:
    def __init__(self):
       self.button = False
       self.button2 = False
       rospy.Subscriber('/my_touch_sensor_right', Contact, self.callback)
       rospy.Subscriber('/my_touch_sensor_left', Contact, self.callback2)
   
    def callback(self, data):
       self.button = data.contact
    
    def callback2(self, data):
       self.button2 = data.contact


def main():
   rospy.init_node('nxt_control')
   pub = rospy.Publisher('/joint_command', JointCommand, queue_size = 3)
   jointCmd = JointCommand()
   rate = rospy.Rate(5)
   myCtrl = nxtController()
   jointCmd.name = 'motor_joint'
   jointCmd.effort = 1.0
   pub.publish(jointCmd)
   rate.sleep()

   while not rospy.is_shutdown():
     if myCtrl.button2 == True:
       print 'touched left'
     if myCtrl.button == True:
       print 'touched right'
       if jointCmd.effort == 1.0:
         pass
         #jointCmd.effort = -1.0
       elif jointCmd.effort == -1.0:
         pass
         #jointCmd.effort = 1.0
       #pub.publish(jointCmd)
       #rate.sleep()

if __name__ == '__main__':
    try:
       main()
    except rospy.ROSInterruptException:
       pass
