Research Track 1: first Assignment
================================

Here in this repository you can find the python code for the first assignment of the course Research Track 1,
done by Carlos Ángel López de Rodas Serrano.
It uses the robot simulator developed by [Student Robotics](https://studentrobotics.org).


Running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

When done, you can run the code with:

```bash
$ python2 run.py assignment1.py
```

## Code description
-----------------------------

The code drives the robot around a circuit grabing the silver tokens it comes across and avoiding touching the golden tokens.

### Pseudocode ###

The logical behaviour of the code is the following:

```
WHILE True;

	IF (there are golden tokens in front of the car);
	
		IF (the golden tokens on the right of the car are closer than the ones on the left);
			turn left;
		ELSE 
			turn right;
			
	ELSEIF (there is a silver token in front of the car AND there are no golden tokens it the way);
	
		IF (close enough);
			grab the token;
			turn 180 degrees;
			release the token;
			turn 180 degrees;
		ELSEIF (align with the token);
			drive towards the token;
		ELSEIF (not align to the right);
			turn left;
		ELSEIF (not align to the left);
			turn right;
			
	ELSE;
		drive the car forwards;
```


To implement this code, some constants and functions had to be defined.

### Constants ###

* `a_th` (float): threshold to grab the silver token. It indicates when the car is close enough to the silver token.
* `d_th` (float): it defines the front of the car angle range.
* `t_th` (float): it defines the front of the car, distance range.
* `g_th` (float): distance at which a silver token can be detected.
* `ag_th` (float): angle range for alignment with the silver tokens.
* `speed` (float): speed of the wheels.
* `width` (float): width of the car.

### Functions ###

* Two functions to move the robot around where defined:

```python
  def drive(speed, seconds):
  def turn(speed, seconds):
```
  It is possible to control the direction of the turn by the sign of the variable ``speed`` (+ turns to the right/ - turns to the left)


* A function to determine whether there are golden tokens or not, is defined:

```python
  def vision_delantera(d_th, dist):
```

  This function will search for any golden token in a certain range.
  It returns ``True`` if there are no golden tokens in that range, ``False`` otherwise.


* To determine if a silver token is reachable we define this function:

```python
  def silver_token_visible(dist, rot, d_th):
```

  The function will search for silver tokens in a certain range and if it finds it, it will check if there are golden tokens in between.
  If there are golden tokens in between or no silver tokens are found, it will return ``False``, otherwise, it will return ``True``


* If a silver token is reachable, the code that describes the behaviour to be performed is compacted in the next function:

```python
  def silver(dist, rot, s, a, d, w, pi):
```

  This function will drive the car towards the silver token. When it reaches the token, another function is executed:
  
```python
  def voltereta(speed, w, pi):
```

  This function will grab the token, turn 180 degree, release the token and turn back to continue its jurney.
  
  
* The last function needed for the code is folowing:

```python
  def vision_lateral_coche():
```

  This will compare the distance of the golden tokens on the right side and the left side of the car. 
  It returns ``+1`` if the tokens are closer on the left side and ``-1`` otherwise.
  
## Psible improvements
-----------------------------

The main problem with this code (regarding runnig time) is the fact that, when no silver token is visible, a couple of nested ``for`` loops have to be entirely performed:

```python
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
```

This ``for`` loop is calling the function ``silver_token_visible`` (which has a ``for`` loop inside) each loop. 

This can be improve by trying a more efficient loop structure to reduce the computation time or even trying to redefine the concept of "silver token visible" so no nested loops are required.







