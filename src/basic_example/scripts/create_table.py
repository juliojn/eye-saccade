#!/usr/bin/python3.7
from std_msgs.msg import String
import opensim as osim
import rospy
import numpy as np
import math
import sys
import os
import system_variables as sv

model = osim.Model()
state = osim.State()
brain = osim.PrescribedController()
eye_add_abd = osim.Coordinate()
manager = osim.Manager()

def loadSystem():
	# ----------------------------------------------------------------------
	# Load the musculoskeletal model from a file.
	# ----------------------------------------------------------------------

	global model, state, brain, eye_add_abd, manager
	path = os.path.dirname(os.path.abspath(__file__))
	model = osim.Model(path + "/../model/UPAT_Eye_Model_Passive_Pulleys.osim")

	# ----------------------------------------------------------------------
	# Add a controller to the model's muscles.
	# ----------------------------------------------------------------------

	actuator_set = model.getActuators()
	lateral_rectus = actuator_set.get("r_Lateral_Rectus")
	medial_rectus  = actuator_set.get("r_Medial_Rectus")

	brain.addActuator(lateral_rectus)
	brain.addActuator(medial_rectus)

	brain.prescribeControlForActuator("r_Lateral_Rectus", osim.Constant(0.0))
	brain.prescribeControlForActuator("r_Medial_Rectus", osim.Constant(0.0))
	model.addController(brain)

	coordinate_set = model.getCoordinateSet()
	eye_add_abd = coordinate_set.get("r_eye_add_abd")

	# --------------------------------------------------------------------------
	# Configure the simulation of the model
	# --------------------------------------------------------------------------

	state = model.initSystem()
	model.equilibrateMuscles(state)
	state.setTime(0.0)
	manager = osim.Manager(model)
	manager.initialize(state)

# --------------------------------------------------------------------------
# Gauss function to calculate the desirable speed
# --------------------------------------------------------------------------

def gauss(x, total_time, angle):
	rad_angle = math.radians(angle)
	b = (total_time * 0.9) / 2
	c = 1/6 * (total_time * 0.9)
	a = rad_angle / (np.sqrt(2) * c * np.sqrt(math.pi))
	return a * math.exp(-((x - b)**2) / (2 * c**2))


# if __name__ == "__main__":
def getTable(total_time, angle):
	global model, state, brain, eye_add_abd, manager
	time = 0.0				# in seconds
	# Error in absolute value, lateral_control_signal and medial_control_signal
	table = []
	steps = 15

	loadSystem()

	while time <= total_time:
		time += sv.sim_time
		goal_speed = gauss(time, total_time, angle)
		# Minimum and maximum value for the related muscle controller
		min = 0.0
		max = 1.0
		lateral_signal = 0.0
		medial_signal = 0.0

		idle_state = osim.State(state)
		brain.prescribeControlForActuator("r_Lateral_Rectus", osim.Constant(lateral_signal))
		brain.prescribeControlForActuator("r_Medial_Rectus", osim.Constant(medial_signal))
		manager = osim.Manager(model, idle_state)
		idle_state = manager.integrate(time)
		idle_speed = eye_add_abd.getSpeedValue(idle_state)

		for i in range(0, steps):
			new_state = state
			manager = osim.Manager(model, new_state)

			mean = (max + min) / 2
			# --------------------------------------------------------------
			# If the next speed to reach is higher than the current speed,
			# only the medial rectus is activated to increase the angular
			# speed around the positive direction of the Y-axis.
			# Otherwise, only the lateral rectus is activated.
			# --------------------------------------------------------------
			if (goal_speed > idle_speed):
				lateral_signal = 0.0
				medial_signal = mean
			else:
				lateral_signal = mean
				medial_signal = 0.0

			brain.prescribeControlForActuator("r_Lateral_Rectus", osim.Constant(lateral_signal))
			brain.prescribeControlForActuator("r_Medial_Rectus", osim.Constant(medial_signal))
			new_state = manager.integrate(time)
			new_speed = eye_add_abd.getSpeedValue(new_state)

			if (goal_speed > idle_speed):
				# It is still needed to increase the control signal
				if (goal_speed > new_speed):
					min = mean
				# It is needed to decrease the control signal
				else:
					max = mean
			else:
				# It is still needed to increase the control signal
				if (goal_speed < new_speed):
					min = mean
				# It is needed to decrease the control signal
				else:
					max = mean

		mean = (max + min) / 2
		if (goal_speed > idle_speed):
			lateral_signal = 0.0
			medial_signal = mean
		else:
			lateral_signal = mean
			medial_signal = 0.0
		brain.prescribeControlForActuator("r_Lateral_Rectus", osim.Constant(lateral_signal))
		brain.prescribeControlForActuator("r_Medial_Rectus", osim.Constant(medial_signal))
		state = osim.State(manager.integrate(time))

		table.append(np.array((time, lateral_signal, medial_signal), dtype="float"))

		print("%s\t%s\t%s"%(state.getTime(), lateral_signal, medial_signal))
	position = eye_add_abd.getValue(state)
	print("Final position (in degrees): %s"%math.degrees(position))
	return table
