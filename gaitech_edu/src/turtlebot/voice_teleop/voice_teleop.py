#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class RobotVoiceTeleop:
    #define the constructor of the class
    def  __init__(self):
        #initialize the ROS node with a name voice_teleop
        rospy.init_node('voice_teleop')
        
        # Publish the Twist message to the cmd_vel topic
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        
        # Subscribe to the /recognizer/output topic to receive voice commands.
        rospy.Subscriber('/Rog_result', String, self.voice_command_callback)
        
        #create a Rate object to sleep the process at 5 Hz
        rate = rospy.Rate(5)
        
        # Initialize the Twist message we will publish.
        self.cmd_vel = Twist()
        #make sure to make the robot stop by default
        self.cmd_vel.linear.x=0;
        self.cmd_vel.angular.z=0;
        
        
        
        # A mapping from keywords or phrases to commands
        #we consider the following simple commands, which you can extend on your own
        self.commands =             ['停止',
                                    '前进',
                                    '后退',
                                    '左转',
                                    '右转',
                                    ]
        rospy.loginfo("Ready to receive voice commands")
        # We have to keep publishing the cmd_vel message if we want the robot to keep moving.
        while not rospy.is_shutdown():
            self.cmd_vel_pub.publish(self.cmd_vel)
            rate.sleep()


    def voice_command_callback(self, msg):
        # Get the motion command from the recognized phrase
        command = msg.data
        if (command in self.commands):
            if command == '前进':
                self.cmd_vel.linear.x = 0.1
                self.cmd_vel.angular.z = 0.0
            elif command == '后退':
                self.cmd_vel.linear.x = -0.1
                self.cmd_vel.angular.z = 0.0
            elif command == '左转':
                self.cmd_vel.linear.x = 0.0
                self.cmd_vel.angular.z = 0.5
            elif command == '右转':
                self.cmd_vel.linear.x = 0.0
                self.cmd_vel.angular.z = -0.5
            elif command == '停止':
                self.cmd_vel.linear.x = 0.0
                self.cmd_vel.angular.z = 0.0

       # else: #command not found
            #print 'command not found: '+command
        #    self.cmd_vel.linear.x = 0.0
        #    self.cmd_vel.angular.z = 0.0
        print ("linear speed : " + str(self.cmd_vel.linear.x))
        print ("angular speed: " + str(self.cmd_vel.angular.z))



if __name__=="__main__":
    try:
      RobotVoiceTeleop()
      rospy.spin()
    except rospy.ROSInterruptException:
      rospy.loginfo("Voice navigation terminated.")
