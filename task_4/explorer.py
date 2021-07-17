#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Twist
from tf.transformations import euler_from_quaternion
import math
import random
from sensor_msgs.msg import LaserScan

x=0.0
y=0.0
theta=0.0
countd=0 #count for the distance travelled
counta=0 #count for the angle rotated
sdist=0.0 #shortest distance from an obstacle
distances=[0]*360 #distances in a 90 degree range in front of the bot
angle=0.0
countc=0 #count for choosing the next direction while exploring

#def forward():


def callback(msg):
	global x
	global y
	global theta

	x=msg.pose.pose.position.x
	y=msg.pose.pose.position.y
	rot_q=msg.pose.pose.orientation
	(roll, pitch, theta)=euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])#returns the euler angle from the quaternion
	if theta<0:
		theta+=(2*math.pi)
	

def ScanCallback(msg):
	global distances
	distances=msg.ranges

def main():
	global countd
	global counta
	global countc
	global distances
	global angle
	global theta

	rospy.init_node("explorer")
	sub = rospy.Subscriber("odom", Odometry, callback)
	pub=rospy.Publisher("cmd_vel", Twist, queue_size=1)

	speed=Twist()
	r=rospy.Rate(4)

	a=random.randint(5,20)
	b=random.randint(10,21)

	scan_sub=rospy.Subscriber("scan", LaserScan, ScanCallback)
	
	# main logic is that the bot travels in a region of direction where the minimum range is the maximum out of all the other minimums

	while not rospy.is_shutdown():

		close = min(distances[0:359])<0.3
		touching = min(distances[0:359])<0.15
		#rospy.loginfo("Min:{}".format(min(distances[0:359])))

		if touching:
			speed.linear.x=-0.5
			angle=random.randint(0, 360) #in case the bot does not get stuck in a repetitive loop of going back and forth
		
		if countd<a and not (close or touching):
			speed.linear.x=0.25
			speed.angular.z=0
			countd+=1
			countc=0
			rospy.loginfo("not close")

		if close and not touching: #3 logics for dealing with this: max of minimums of the region, randomly turn another direction, go in the direction of maximum range
			speed.linear.x=0

			#rospy.loginfo("Hello there")
			if countc<1:
				speed.linear.x=-0.5

				mins=[min(distances[316:359]+distances[0:45]), min(distances[46:135]), min(distances[136:225]), min(distances[226:315])]
				max_dir = distances.index(max(mins)) #-direction of the region with the fathest minimum range

				################# max of mins ##################### combined with regions
				if max_dir > 45 and max_dir<136:
					angle=distances.index(min(distances[46:136]))
				elif max_dir > 135 and max_dir<226:
					angle=distances.index(min(distances[136:226]))
				elif max_dir > 225 and max_dir<316:
					angle=distances.index(min(distances[226:316]))
				#rospy.loginfo("max_dir:{}".format(max_dir))
				#angle=distances.index(max(distances))
				
				################## random backwards angle ################
				"""start=int(theta+90)
				stop=int(theta+270)

				if start<360 and stop<360:
					angle=random.randint(start, stop)
				elif start<360 and stop>360:
					angle=random.randint(start,360)
				else:
					angle=random.randint(start-360, stop-360)	"""

				countc+=1
				#rospy.loginfo("angle:{}".format(angle))

			rospy.loginfo("min:{}".format(distances.index(min(distances))))				
			rospy.loginfo("angle:{}, theta:{}".format(angle, 180*theta/math.pi))	
			pointing_correctly = abs(180*theta/math.pi-angle)<5
			if not pointing_correctly:
				speed.angular.z=0.25
			if pointing_correctly: #start moving away from the obstacle
				speed.angular.z=0
				speed.linear.x=0.1
				countd=0
				a=random.randint(5,20)

		pub.publish(speed)
		r.sleep()


if __name__ == '__main__':
	main()
