import time
import sys
from math import pi, degrees
from .world import World
from .constants import RPS_PER_PERCENTAGE, WHEEL_DIAMETER, PIXELS_PER_METER
from typing import Callable


class RobotOutOfBounds(Exception):
    pass


class Timeout(Exception):
    pass


class PiBot:
    """
    PiBot class

    Attributes
    ----------
    track_image: str
        Path to the track image the bot will be on.
    starting_orientation: int
        The starting rotation of the robot, defaults to -90 (points to north)
    start_x: int
        X coordinate where robot will start.
    start_y: int
        Y coordinate where robot will start.
    timeout: int
        Sleep time until robot raises Timeout exception.

    Sensors:
              3    4
            2        5
          1            6
    """
    def __init__(
            self,
            track_image: str = 'track.png',
            starting_orientation: int = -90,
            start_x: int = 250,
            start_y: int = 450,
            timeout: int = 30,
    ):
        self._left_rps = 0
        self._right_rps = 0

        self._world = World(track_image, starting_orientation, start_x, start_y)

        # variable used to keep track of real time taken
        self._time_start = time.time()

        # variable used to keep track of sleep time
        self.time_from_start = 0
        self._timeout = timeout
        self.steps_taken = 0

    def __getattribute__(self, item):
        """Magic method implemented to count the number of function calls made directly by the user."""
        obj = super().__getattribute__(item)
        previous_frame = sys._getframe(1)
        if isinstance(obj, Callable) and not item.startswith('_') and previous_frame.f_code.co_filename != __file__:
            self.steps_taken += 1

        return obj

    def set_left_wheel_speed(self, percentage: float) -> None:
        """
        Set the left wheel speed.

        :parameter percentage: Speed percent from 0.0% to 100.0%
        """
        if not -100 <= percentage <= 100:
            raise Exception('Robot wheels speed can\'t go above 100%')

        self._left_rps = RPS_PER_PERCENTAGE * percentage

    def set_right_wheel_speed(self, percentage: float) -> None:
        """
        Set the right wheel speed.

        :parameter percentage: Speed percent from 0.0% to 100.0%
        """
        if not -100 <= percentage <= 100:
            raise Exception('Robot wheels speed can\'t go above 100%')

        self._right_rps = RPS_PER_PERCENTAGE * percentage

    def set_wheels_speed(self, percentage: float) -> None:
        """
        Set the speed for both wheels

        :parameter percentage: Speed percent from 0.0% to 100.0%
        """
        if not -100 <= percentage <= 100:
            raise Exception('Robot wheels speed can\'t go above 100%')

        self.set_left_wheel_speed(percentage)
        self.set_right_wheel_speed(percentage)

    def sleep(self, sleep_time: float) -> None:
        """
        Sleep after the parameters have been set and allow the bot to move for sleep_time seconds

        :param sleep_time: How long the bot should move.
        :raises Timeout: If the total time spent moving exceeds _timeout
        :raises RobotOutOfBounds: If the robot moves outside of the bounds of the track image.
        """
        if sleep_time <= 0 or self._world.done:
            return

        velocity1 = self._left_rps * WHEEL_DIAMETER * pi
        velocity2 = self._right_rps * WHEEL_DIAMETER * pi

        self._world.move(velocity1 * sleep_time, velocity2 * sleep_time)

        # set a cap on the time the bot can sleep/move, otherwise it might get stuck in a loop
        self.time_from_start += sleep_time
        if self.time_from_start > self._timeout:
            self.done()
            raise Timeout('The robot timed out')

        if self._world.is_robot_out_of_bounds():
            self.done()
            raise RobotOutOfBounds('The robot has moved out of bounds')

    def get_left_line_sensor(self) -> int:
        """
        Value of the pixel under the sensor 3

        :returns: int that 0 (black) to 1024 (white)
        """
        return self._world.sensor_value_at(-0.01, 0.03)

    def get_second_line_sensor_from_left(self) -> int:
        """
        Value of the pixel under the sensor 2

        :returns: int that 0 (black) to 1024 (white)
        """
        return self._world.sensor_value_at(-0.02, 0.02)

    def get_third_line_sensor_from_left(self) -> int:
        """
        Value of the pixel under the sensor 1

        :returns: int that 0 (black) to 1024 (white)
        """
        return self._world.sensor_value_at(-0.03, 0.01)

    def get_right_line_sensor(self) -> int:
        """
        Value of the pixel under the sensor 4

        :returns: int that 0 (black) to 1024 (white)
        """
        return self._world.sensor_value_at(0.01, 0.03)

    def get_second_line_sensor_from_right(self) -> int:
        """
        Value of the pixel under the sensor 5

        :returns: int that 0 (black) to 1024 (white)
        """
        return self._world.sensor_value_at(0.02, 0.02)

    def get_third_line_sensor_from_right(self) -> int:
        """
        Value of the pixel under the sensor 6

        :returns: int that 0 (black) to 1024 (white)
        """
        return self._world.sensor_value_at(0.03, 0.01)

    def get_left_line_sensors(self) -> list[int]:
        """
        Values of the sensors on the left side.

        :return: List[int]
        """
        return [
            self.get_left_line_sensor(),
            self.get_second_line_sensor_from_left(),
            self.get_third_line_sensor_from_left()
        ]

    def get_right_line_sensors(self) -> list[int]:
        """
        Values of the sensors on the right side.

        :return: List[int]
        """
        return [
            self.get_right_line_sensor(),
            self.get_second_line_sensor_from_right(),
            self.get_third_line_sensor_from_right()
        ]

    def get_line_sensors(self) -> list[int]:
        """
        Values of all the sensors on the bot.
        :return: List[int]
        """
        return self.get_left_line_sensors() + self.get_right_line_sensors()

    def get_rotation(self) -> int:
        """
        Degress of rotation of the bot.
        :return: Rotation degrees in value
        """
        return int(degrees(self._world.robot_phi))

    def get_position(self) -> tuple:
        """
        The position of the robot on the track.
        :return tuple: (x, y) coordinates of the robot
        """
        return round(self._world.robot_x * PIXELS_PER_METER), round(self._world.robot_y * PIXELS_PER_METER)

    def _time_taken(self) -> float:
        """
        The amount of real time taken to execute to program in seconds.
        :return: float
        """
        end = time.time()
        return end - self._time_start

    def done(self, save_image: str = "robot_path.png"):
        """
        Function to call when the bot runner is done.
        :param str save_image: path where to save the path taken image.
        """
        self._world.done = True
        self._world.turtle.draw_robot(self._world.robot_x, self._world.robot_y)

        print(f'Real time taken to complete: {round(self._time_taken() * 1000)}ms')
        print(f'Sleep time taken to complete: {round(self.time_from_start)}s')
        print(f'steps taken to complete: {self.steps_taken}')

        self._world.save_image(save_image)
