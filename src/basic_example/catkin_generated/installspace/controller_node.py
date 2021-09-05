#!/usr/bin/python3.7
from std_msgs.msg import String
from basic_example.srv import *
import rospy
import sys
import os

def getError(current_pos, time):
	goal_pos = 0.5
	error = goal_pos - req.current_pos
	print("%s %s"%(req.time, error))
	return GetErrorResponse(error)

def get_control_signal_handler(req):
	print("[%s, %s]"%(req.current_pos, req.time))

	error = getErrorClient(req)
	if error > 0.0:
		return GetControlSignalResponse(0.0, 1.0)
	else:
		return GetControlSignalResponse(1.0, 0.0)

def get_control_signal():
	rospy.init_node("get_control_signal")
	s = rospy.Service("get_control_signal", GetControlSignal, get_control_signal_handler)
	rospy.spin()


if __name__ == "__main__":
	get_control_signal()
