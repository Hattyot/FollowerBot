import os
from math import sin, cos, pi, radians
from PIL import ImageDraw, Image
from .constants import PIXELS_PER_METER, AXIS_LENGTH, VALUE_PER_ALPHA, SENSORS


class World:
    """
    The world which the robot exists in.

    Attributes
    ----------
    track_image: str
        Path to the track image the bot will be on.
    start_x: int
        X coordinate where robot will start.
    start_y: int
        Y coordinate where robot will start.

    """
    def __init__(self, track_image: str, starting_orientation: int, start_x: int, start_y: int):
        self.robot_x = start_x/PIXELS_PER_METER
        self.robot_y = start_y/PIXELS_PER_METER
        self.robot_path = [(round(self.robot_x * PIXELS_PER_METER), round(self.robot_y * PIXELS_PER_METER))]

        self.robot_phi = radians(starting_orientation)  # robot rotation in radians

        if not os.path.exists(track_image):
            raise Exception(f'Unable to find a track image: "{track_image}"')

        self.track_image_path = track_image
        self.track_image = Image.open(track_image).convert("L")
        self.turtle = Turtle(track_image, self)

        self.done = False

        self.robots = []

        # draw initial point, otherwise it's only drawn after the first movement
        self.turtle.point_at(round(self.robot_x * PIXELS_PER_METER), round(self.robot_y * PIXELS_PER_METER))

    def save_image(self, path: str = 'robot_path.png'):
        """
        Saves the world image.

        :parameter path: name of the images.
        """
        self.turtle.save_image(path)

    def move(self, left_delta, right_delta):
        """
        Moves the robot inside the world.

        :param left_delta: distance moved by the left wheel
        :param right_delta: distance moved by the right wheel
        """
        if self.done:
            return

        if abs(left_delta - right_delta) < 1e-6:
            self.robot_x += left_delta * cos(self.robot_phi)
            self.robot_y += left_delta * sin(self.robot_phi)
        else:
            R = AXIS_LENGTH * (left_delta + right_delta) / (2 * (right_delta - left_delta))
            rotation_change = (right_delta - left_delta) / AXIS_LENGTH
            self.robot_x += R * sin(rotation_change + self.robot_phi) - R * sin(self.robot_phi)
            self.robot_y += - R * cos(rotation_change + self.robot_phi) + R * cos(self.robot_phi)
            self.robot_phi += rotation_change

        pixel_cords = (round(self.robot_x * PIXELS_PER_METER), round(self.robot_y * PIXELS_PER_METER))
        self.robot_path.append(pixel_cords)

        # red robot dot
        self.turtle.point_at(*pixel_cords)

    def _ground_value_at(self, x, y) -> int:
        """
        Calculates the value at position x, y
        :param x: x axis coordinate on the track
        :param y: y axis coordinate on the track
        :return: int value ranging from 0 (white) to 1024 (black)
        """
        self.turtle.point_at(
            round(x * PIXELS_PER_METER),
            round(y * PIXELS_PER_METER),
            "green"
        )
        return int(
            self.track_image.getpixel((
                min(
                    max(round(x * PIXELS_PER_METER), 0),
                    self.track_image.width - 1
                ),
                min(
                    max(round(y * PIXELS_PER_METER), 0),
                    self.track_image.height - 1
                )
            )) * VALUE_PER_ALPHA
        )

    def is_robot_out_of_bounds(self) -> bool:
        """
        Checks if the robot has moved out of bounds

        :returns bool: True if robot has moved outside of bounds, False if not
        """
        return self.robot_x < 0 or \
               self.robot_y < 0 or \
               self.robot_x * PIXELS_PER_METER > self.track_image.width or \
               self.robot_y * PIXELS_PER_METER > self.track_image.height

    def point_to_world(self, x, y):
        """
        Calculates location of a point x,y relative to the location and rotation of the robot

        :param x: distance from the robot on the x axis
        :param y: distance from the robot on the y axis
        :return: x,y coordinates of the point in the world.
        """
        # maths for point rotation around origin
        s = cos(-self.robot_phi)
        c = sin(-self.robot_phi)
        x_new = x * c + y * s
        y_new = x * s - y * c

        return self.robot_x + x_new, self.robot_y + y_new

    def sensor_value_at(self, x, y):
        """
        Get the value under given sensor.

        :param x: sensor's distance from the robot on the x axis
        :param y: sensor's distance from the robot on the y axis
        :return:
        """
        s = cos(-self.robot_phi)
        c = sin(-self.robot_phi)
        x_new = self.robot_x + (x * c + y * s)
        y_new = self.robot_y + (x * s - y * c)

        return self._ground_value_at(x_new, y_new)


class Turtle:
    """
    The turtle that does the drawing.
    """
    def __init__(self, base_image, world, *, colour: str = 'red'):
        self.image = Image.open(base_image)
        self.drawing = ImageDraw.Draw(self.image)

        self.color = colour

        self.x = self.image.width / 2
        self.y = self.image.height / 2
        self.phi = -pi / 2

        self.world: World = world

    def save_image(self, name):
        """Save the newly created image."""
        self.image.save(name)

    def point_at(self, x: int, y: int, color=None):
        """
        Draw a point at x, y coordinates.

        :param x: point on the x axis of the images
        :param y: point on the y axis of the image
        :param color: Optional colour
        """
        if color is None:
            color = self.color

        self.x = x
        self.y = y
        self.drawing.point([self.x, self.y], color)

    def draw_robot(self, loc_x: float, loc_y: float):
        """
        Draws the cute little robot on the image.

        :param loc_x: location of the bot on the x axis
        :param loc_y: location of the bot on the y axis
        """
        loc_x = round(PIXELS_PER_METER * loc_x)
        loc_y = round(PIXELS_PER_METER * loc_y)

        sensor_points = [self.world.point_to_world(*s) for s in SENSORS]

        radius = AXIS_LENGTH * PIXELS_PER_METER / 3
        self.drawing.ellipse(
            [
                round(loc_x - radius),  # left side
                round(loc_y - radius),  # front
                round(loc_x + radius),  # right side
                round(loc_y + radius)  # back
            ],
            outline="blue", width=1, fill='white'
        )

        self.point_at(loc_x, loc_y)

        self.drawing.point(
            list(map(
                lambda x: (
                    round(x[0] * PIXELS_PER_METER),
                    round((x[1]) * PIXELS_PER_METER)
                ),
                sensor_points
            )),
            fill="green"
        )
