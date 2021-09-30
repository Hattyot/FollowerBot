A simplistic robot simulator based on [https://github.com/iti0201/robot](https://github.com/iti0201/robot), 
Continuation on the work done by tiloom.

## Requirements
* python 3.9

## Install
### Through Git:
```
git clone https://github.com/Hattyot/Pibot.git
pip3 install -e PiBot
```

## Movement methods
These are the functions used to move the bot
```python
set_left_wheel_speed(percentage)
set_right_wheel_speed(percentage)
set_wheels_speed(percentage)
```

## Sensor methods
The PiBot has 6 sensors
```python
#      3    4
#    2        5
#  1            6
get_third_line_sensor_from_left()  # sensor 1
get_second_line_sensor_from_left()  # sensor 2
get_left_line_sensor()  # sensor 3
get_right_line_sensor()  # sensor 4
get_second_line_sensor_from_right()  # sensor 5
get_third_line_sensor_from_right()  # sensor 6
```
You can also get the values of multiple sensors
```python
get_left_line_sensors()  # sensors 1, 2, 3
get_right_line_sensors()  # sensors 4, 5, 6
get_line_sensors()  # all the sensors
```

## Sleeping
After the movement parameters have been set, the sleep function needs to be called to move the robot
```python
sleep(time)
```


## Done
After you've completed the objective with the robot, the done function needs to be called, a picture showing you the path the robot took will be saved
```python
done()
```

## Example
A simple example of a robot that will drive straight for a bit.
```python
from PiBot import PiBot

robot = PiBot()

robot.set_wheels_speed(30)
robot.sleep(2)
robot.set_wheels_speed(0)
robot.done()
```



