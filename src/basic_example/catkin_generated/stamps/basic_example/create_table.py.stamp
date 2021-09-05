#!/usr/bin/python3.7
from std_msgs.msg import String
import opensim as osim
import rospy
import math
import numpy
import sys
import os


# ----------------------------------------------------------------------
# Load the musculoskeletal model from a file.
# ----------------------------------------------------------------------

path = os.path.dirname(os.path.abspath(__file__))
model = osim.Model(path + "/../model/UPAT_Eye_Model_Passive_Pulleys_v2.osim")

# ----------------------------------------------------------------------
# Add a controller to the model's muscles.
# ----------------------------------------------------------------------

actuator_set = model.getActuators()
lateral_rectus = actuator_set.get("r_Lateral_Rectus")
medial_rectus  = actuator_set.get("r_Medial_Rectus")

brain = osim.PrescribedController()
brain.addActuator(lateral_rectus)
brain.addActuator(medial_rectus)

brain.prescribeControlForActuator("r_Lateral_Rectus", osim.Constant(0.0))
brain.prescribeControlForActuator("r_Medial_Rectus", osim.Constant(0.0))
model.addController(brain)

# ----------------------------------------------------------------------
# Add a console reporter to print the following values:
# 	Position and speed of the adduction-abduction rotational Degree of
# 	Freedom (y-axis).
# 	Current fiber force  applied to the Lateral Rectus and the
# 	Medial Rectus tendons.
# ----------------------------------------------------------------------

coordinate_set = model.getCoordinateSet()
eye_add_abd = coordinate_set.get("r_eye_add_abd")
#
# reporter = osim.ConsoleReporter()
# reporter.set_report_time_interval(0.002)
# reporter.addToReport(eye_add_abd.getOutput("value"), "position")
# reporter.addToReport(eye_add_abd.getOutput("speed"), "speed")
# reporter.addToReport(lateral_rectus.getOutput("fiber_force"), "lateral_force")
# reporter.addToReport(medial_rectus.getOutput("fiber_force"), "medial_force")
# model.addComponent(reporter)

# --------------------------------------------------------------------------
# Configure the simulation of the model
# --------------------------------------------------------------------------

state = model.initSystem()
model.equilibrateMuscles(state)
manager = osim.Manager(model)
state.setTime(0)
manager.initialize(state)

# --------------------------------------------------------------------------
# Gauss function to calculate the desirable speed
# --------------------------------------------------------------------------

def gauss(x):
	a = 0.65
	b = 0.5
	c = 0.16
	return a * math.exp(-((x - b)**2) / (2 * c**2))

# --------------------------------------------------------------------------
# Return the error
# --------------------------------------------------------------------------

def getError(time)

if __name__ == "__main__":
	time = 0.0				# in seconds
	sim_time = 0.002		# in seconds

	while time < 1.1:

		while
		# print("%s\t%s"%(time, gauss(time)))
		time += sim_time
