#!/usr/bin/python3.7
from std_msgs.msg import String
import opensim as osim
import rospy
import sys
import os

sim_time = 2.0		# in seconds
simulations = 0


# ----------------------------------------------------------------------
# Load the musculoskeletal model from a file.
# ----------------------------------------------------------------------

path = os.path.dirname(os.path.abspath(__file__))
model = osim.Model(path + "/../model/UPAT_Eye_Model_Passive_Pulleys_v1.osim")

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

reporter = osim.ConsoleReporter()
reporter.set_report_time_interval(0.2)
reporter.addToReport(eye_add_abd.getOutput("value"), "position")
reporter.addToReport(eye_add_abd.getOutput("speed"), "speed")
reporter.addToReport(lateral_rectus.getOutput("fiber_force"), "lateral_force")
reporter.addToReport(medial_rectus.getOutput("fiber_force"), "medial_force")
model.addComponent(reporter)

# --------------------------------------------------------------------------
# Configure the simulation of the model
# --------------------------------------------------------------------------

state = model.initSystem()
model.equilibrateMuscles(state)
manager = osim.Manager(model)
state.setTime(0)
manager.initialize(state)

# --------------------------------------------------------------------------
# Pull only the Lateral Rectus muscle
# --------------------------------------------------------------------------

def pullLateralRectus():
	global simulations

	brain.prescribeControlForActuator("r_Lateral_Rectus", osim.Constant(1.0))
	brain.prescribeControlForActuator("r_Medial_Rectus", osim.Constant(0.0))
	simulations += 1
	time = sim_time * simulations
	manager.integrate(time)

# --------------------------------------------------------------------------
# Pull only the Rectal Rectus muscle
# --------------------------------------------------------------------------

def pullRectalRectus():
	global simulations

	brain.prescribeControlForActuator("r_Lateral_Rectus", osim.Constant(0.0))
	brain.prescribeControlForActuator("r_Medial_Rectus", osim.Constant(1.0))
	simulations += 1
	time = sim_time * simulations
	manager.integrate(time)

if __name__ == '__main__':
	while True:
		pullLateralRectus()
		pullRectalRectus()
