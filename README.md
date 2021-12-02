A simplistic robot simulator based on [https://github.com/iti0201/robot](https://github.com/iti0201/robot).


## Requirements
* python 3.9

## Install
### Through Git:
```bash
git clone https://github.com/Hattyot/FollowerBot.git
pip3 install -e FollowerBot
```
or
```bash
pip3 install git+https://github.com/Hattyot/FollowerBot.git#egg=FollowerBot
```


# The little robot that could
The robot has radius of 5px \
It has 6 sensors in this configuration.
```
      3    4
    2        5
  1            6
```
The sensors are always seperated by 1-2px

## Methods
### Movement methods
These are the functions used to move the bot
```python
set_left_wheel_speed(percentage)
set_right_wheel_speed(percentage)
set_wheels_speed(percentage)
```

### Sensor methods
The FollowerBot has 6 sensors\
ranges from 0 (black) to 1024 (white)
```python
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

### Position
Find out the robot's position on the given track.\
The returned coordinates are in pixels.\
There are 100 pixels in a meter.
```python
get_position()
```

### Sleeping
After the movement parameters have been set, the sleep function needs to be called to move the robot
```python
sleep(time: float)
```

### Done
After you've completed the objective with the robot, the done function needs to be called, a picture showing you the path the robot took will be saved
```python
done()
```

## Track
the track the bot runs on can be any image. Track image path can be specified in the FollowerBot class args.

## Example
A simple example of a robot that will drive straight for a bit.
```python
from FollowerBot import FollowerBot

robot = FollowerBot()

robot.set_wheels_speed(30)
robot.sleep(2)
robot.set_wheels_speed(0)
robot.done()
```



