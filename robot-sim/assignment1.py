from __future__ import print_function
import time
import math
from sr.robot import *


# ====== CONSTANT DEFINITIONS ======

a_th = 0.4
""" float: Threshold for the control of the linear distance """

d_th = 70.0
""" float: Threshold for angle for the turn """

t_th = 1.5
""" float: Threshold for distance for the forward vision """

g_th = 6.0
""" float: Threshold for distance for the detection of a silver token """

ag_th = 1.5
""" float: Threshold for the angle orientation """

speed = 50.0
""" float: desired speed of the robot """

width = 76.4
""" float: with of the robot """

pi = 3.14159265359

R = Robot()
""" instance of the class Robot """


# ====== FUNCTIONS DEFINITION ======

def drive(speed, seconds):

    	"""
    	Function for setting a linear velocity

    	Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    	"""
    	
    	R.motors[0].m0.power = speed
    	R.motors[0].m1.power = speed
    	time.sleep(seconds)
    	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def turn(speed, seconds):

    	"""
    	Function for setting an angular velocity
    
    	Args:   speed (int): the speed of the wheels
		seconds (int): the time interval
    	"""
    	
    	R.motors[0].m0.power = speed
    	R.motors[0].m1.power = -speed
    	time.sleep(seconds)
    	R.motors[0].m0.power = 0
    	R.motors[0].m1.power = 0
    	
def silver_token_visible(dist, rot, d_th):

	"""
	Function to decide whether a silver token placed at the front of the car (in range +d_th/3, -d_th/3 degrees)
	is visible (return True) or not (return False), which means no golden tokens are closer to the car
	
	Args:   dsit (float): distance from the silver token to the car
		rot (float): angle of the silver token with respect to the car
		d_th (float): angle of the range to decide if the token is in front of the car
	
	Returns:
		True: if the token is visible
		False: if the token is not visible
	"""
	
	for token in R.see():
		if abs(rot) < d_th/3:
			if token.info.marker_type is MARKER_TOKEN_GOLD:
				if (rot-4) < token.rot_y < (rot+4):
					if token.dist < dist:
						return False  # no silver token visible ahead
					else:
						return True   # si silver token visible ahead
		else:
			return False  # no silver token visible ahead
		
def voltereta(speed, w, pi):

	"""
	Funtion for performing the grab(), turn(), release(), turn() 
	
	Args:   speed (float): desired speed of the movement
		w (float): width of the car
		pi (float): number PI
	"""
	
	tiempo = (pi*w/2)/(2*speed)	# to compute the time to make a 180 degrees turn
	print("Yuju! Me doy la vuelta!")
	R.grab()
	turn(speed, tiempo)
	R.release()
	turn(-speed, tiempo)

def silver(dist, rot, s, a, d, w, pi):

	"""
	Function to aligne the car with the silver token, go for it and perform the function voltereta()
	
	Args:   dist (float): distance from the silver token to the car
		rot (float): angle of the silver token with respect to the car
		s (float): desired speed of the movement
		a (float): range for the alignment
		d (float): threshold of the distance for the voltereta() function to be activated
		w (float): width of the car
		pi (float): number PI
	"""
	
	if dist < d:	# if the token is close enough -> voltereta()
		voltereta(s, w, pi)
	elif -a <= rot <= a:	# else, if aligned -> go for it
		drive(s, 0.1)
	elif rot < -a:	# else, if misaligned to the right -> turn left a little bit
		turn(-s/6, 0.1)
	elif rot > a:	# else, if misaligned to the left -> turn right a little bit
		turn(s/6, 0.1)
		
def vision_lateral_coche():

	"""
	Function to compare the distance between the golden tokens at the right side of the car with the golden tokens of the left side
	
	Returns:
		-1: if the distance is smaller on the RIGHT side
		+1: if the distance is smaller on the LEFT side 
	"""
	
	dist_dch = 100
	dist_izq = 100
	
	for token in R.see():
		if token.info.marker_type is MARKER_TOKEN_GOLD:
			if -100 < token.rot_y < -80 and token.dist < dist_izq:
				dist_izq = token.dist
			if 80 < token.rot_y < 100 and token.dist < dist_dch:
				dist_dch = token.dist

	if dist_dch < dist_izq:			
		return -1
	else:
		return 1

def vision_delantera(d_th, dist):

	"""
	Function to see if there are any golden tokens in front of the car
	
	Args:   d_th (float): range of the angle (+d_th, -d_th)
		dist (float): range of the distance
	
	Returns:
		True: if there are NO golden tokens ahead
		False: if there are golden tokens ahead
	"""
	
	a = 0
	
	for token in R.see():
		if token.info.marker_type is MARKER_TOKEN_GOLD and token.dist <= dist:
			if abs(token.rot_y) < d_th/1.5:
				a = 1	# obstacles ahead
			
	if a == 1:	# if obstacles
		return False
	else:
		return True


# ====== MAIN CODE HERE ======

while 1:	# to keep the robot moving at any time

	algo = vision_delantera(d_th, 1)	# let's see what is in front
	
	for token in R.see():	# to check if there are silver tokens visible in front of the car (ss = True if they are and ss = False if they aren't)
		if  token.info.marker_type is MARKER_TOKEN_SILVER and silver_token_visible(token.dist, token.rot_y, d_th):
			if token.dist < g_th:	# the car can only see silver tokens that are 6[-] close
				ss = True
				rot_silver = token.rot_y
				dist_silver = token.dist
				break
			else:
				ss = False
		else:
			ss = False


	if not algo:	# if a golden token is in front
		print("Watch the wal!!")   
		if giro:
			b = vision_lateral_coche()	# turn left or right depending on the distante between the car and the golden tokens on its sides
			giro = False
		turn(b*speed/2, 0.1)
	elif ss:	# if golden token visible 
		giro = True
		print("Silver Token detected")
		silver(dist_silver, rot_silver, speed, ag_th, a_th, width, pi)	# go for the silver token and perform the voltereta()
	else:	# if there are no golden nor silver tokens ahead, then drive forwards
		giro = True
		print("Nothing ahead")
		drive(speed, 0.1)












