#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Point, Twist
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import Imu
from matplotlib import pyplot

x=0.0
y=0.0
z=0.0
time=0

"""def callback(msg):
	x=msg.pose.pose.position.x
	y=msg.pose.pose.position.y
	rot_q=msg.pose.pose.orientation
	(roll, pitch, theta)=euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])#returns the euler angle from the quaternion"""

def ImuCallback(msg):
	global x
	global y
	global z
	x = msg.linear_acceleration.x
	y = msg.linear_acceleration.y
	z = msg.linear_acceleration.z

def main():
	global x
	global y
	global z
	global time

	rospy.init_node("linear_acclog")
	r=rospy.Rate(1)

	file1=open("lin_acclog.txt", "w")

	imu_sub=rospy.Subscriber("imu", Imu, ImuCallback)

	x1=[]
	y1=[]
	z1=[]
	time1=[]
	
	while not rospy.is_shutdown():
		file1.write("x:{}, y:{}, z:{}\n".format(x,y,z))

		x1=x1+[x]
		y1=y1+[y]
		z1=z1+[z]
		time1=time1+[time]

		pyplot.plot(time1, x1)
		pyplot.plot(time1, y1)
		pyplot.plot(time1, z1)
		pyplot.ylabel('Linear acceleration')
		
		pyplot.legend(["x", "y", "z"])
		pyplot.show()
		pyplot.close()

		time+=1
		r.sleep()



if __name__ == '__main__':
	main()
