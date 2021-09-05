#!/usr/bin/python3.7
from std_msgs.msg import String
from basic_example.srv import *
import rospy
import sys
import os

def get_error_handler(req):
	goal_pos = 0.5
	error = goal_pos - req.current_pos
	print("%s %s"%(req.time, error))
	return GetErrorResponse(error)

def get_error():
	rospy.init_node("get_error")
	s = rospy.Service("get_error", GetError, get_error_handler)
	rospy.spin()


if __name__ == "__main__":
	get_error()
