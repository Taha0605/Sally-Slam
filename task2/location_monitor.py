#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
count = 0


def callback(msg):
	x = msg.pose.pose.position.x
	y = msg.pose.pose.position.y
	vel_x = msg.twist.twist.linear.x
	vel_y = msg.twist.twist.linear.y
	if vel_x < 0.05 and vel_y < 0.05:
		rospy.loginfo('x: {}, y: {}'.format(x,y))
	#rospy.loginfo('vel_x: {}, y: {}'.format(vel_x, vel_y))



def main():
	rospy.init_node('location_monitor')
	count += 1
	rospy.Subscriber('/odom', Odometry, callback)
	rospy.loginfo('count:{}'.format(count))
	rospy.spin()

if __name__ == '__main__':
	main()
