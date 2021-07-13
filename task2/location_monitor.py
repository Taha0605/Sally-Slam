#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

x=0.0
y=0.0

count = 0

vel_x=0.0
vel_y=0.0

def callback(msg):
	global x
	global y
	global vel_x
	global vel_y
	x = msg.pose.pose.position.x
	y = msg.pose.pose.position.y
	vel_x = msg.twist.twist.linear.x
	vel_y = msg.twist.twist.linear.y

	#rospy.loginfo('vel_x: {}, y: {}'.format(vel_x, vel_y))



def main():
	global count
	rospy.init_node('location_monitor')
	rospy.Subscriber('/odom', Odometry, callback)
	r=rospy.Rate(1)
	
	while not rospy.is_shutdown():
		if vel_x < 0.05 and vel_y < 0.05 and count==0:
			rospy.loginfo('x: {}, y: {}'.format(x,y))
			count=1
		if vel_x > 0.05 or vel_y > 0.05:
			count=0
		r.sleep()
		

if __name__ == '__main__':
	main()
