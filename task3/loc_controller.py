#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2, sqrtas

x=0.0
y=0.0
theta=0.0

def OdomCallback(msg):
	global x
	global y
	global theta

	x=msg.pose.pose.position.x
	y=msg.pose.pose.position.y
	rot_q=msg.pose.pose.orientation
	(roll, pitch, theta)=euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])#returns the euler angle from the quaternion

def main():
	rospy.init_node("loc_controller")

	sub=rospy.Subscriber("odom", Odometry, OdomCallback)
	pub=rospy.Publisher("cmd_vel", Twist, queue_size=1)

	speed = Twist()#has linear and angular under it

	r=rospy.Rate(30)

	goal = Point()#has position and orientation undr it

	goal = Point()
	goal.x=5
	goal.y=5

	radius = 1 #say for example


	while not rospy.is_shutdown():

		distance = sqrt(((x-goal.x)**2) + ((y-goal.y)**2))

	 	diffx=goal.x-x
	 	diffy=goal.y-y
	 	angle=atan2(diffy,diffx)
		rospy.loginfo('distance: {}, angle: {}'.format(distance, abs(angle-theta)))

		if abs(distance-radius)>0.1 and abs(angle-theta) > 0.1:#abs(angle - theta) shows how much the bot is pointing towards the goal point
	 		speed.linear.x=0.0
	 		speed.angular.z = 0.1

		elif abs(distance-radius)>0.1 and abs(angle-theta) < 0.1:
			speed.linear.x=0.5
			speed.angular.z=0.0

		elif abs(distance-radius)<0.1 and abs(angle-theta)<0.1:#at radius length away and pointing towards the goal point
			speed.linear.x=0.0
	 		speed.angular.z = 0.1#to point perpendicular to the radius

		elif abs(distance-radius)<0.1 and abs(abs(angle-theta)-1.5708)<0.1:#basically at radius length away from point and perpendicular to the radius direction
			if distance > radius:#to revolve around the circle
				speed.angular.z=-0.1
			else:
				speed.angular.z=0.1#increase this to increase the rotation speed of the botwhile it makes its angular corrections while revolving around the goal point
			speed.linear.x=(distance*abs(speed.angular.z))


		pub.publish(speed)
		r.sleep()

if __name__ == '__main__':
	main()
