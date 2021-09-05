#!/usr/bin/python3.7
from std_msgs.msg import String
from basic_example.srv import *
from create_table import getTable
import system_variables as sv
import rospy
import sys
import os

table = []

def get_control_signal_handler(req):
	global table, sim_time, total_time
	i = 0
	while (table[i][0] < (req.time - sv.sim_time / 2)):
		i += 1
	print(table[i][0])
	return table[i][1], table[i][2]


def get_control_signal():
	rospy.init_node("get_control_signal")
	s = rospy.Service("get_control_signal", GetControlSignal, get_control_signal_handler)
	rospy.spin()


if __name__ == "__main__":
	table = getTable(sv.total_time, sv.angle)
	get_control_signal()
