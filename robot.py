from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Callable, List
from alliance import get_alliance_color
from cargo import Cargo
from math import sqrt
from random import random
from field import Hub
if TYPE_CHECKING:
    from field import Field
    from alliance import Alliance
    from graphics import GraphicsArea


class Robot:
    ROBOT_LEN = 0.7

    def __init__(self, position: Tuple[float, float], collect_time: float, shoot_time: float, velocity: float,
                 accuracy: float, alliance: Alliance):
        self.position = position
        self.collect_time = collect_time
        self.shoot_time = shoot_time
        self.velocity = velocity
        self.accuracy = max(min(accuracy, 1), 0)
        self.alliance = alliance
        self.num_cargo = 0

        self.action_time = 0.0
        self.current_action = 0
        self.post_action_time = 0.0
        self.selected_cargo = None
        self.path = None
        self.cycle = [self.select_cargo, self.drive, self.collect_ball, self.shoot_ball]

    def perform_actions(self, field: Field, dt: float):
        """
        The robot performs cycles in the following order:
        collect -> drive -> shoot
        """
        while dt > 0:
            current_action = self.__get_current_action()
            dt -= current_action(field, dt)

    def collect_ball(self, field: Field, dt: float):
        if not self.action_time:
            self.action_time = self.collect_time
        if dt < self.action_time:
            self.action_time -= dt
        elif dt >= self.action_time:
            self.action_time = 0
            dt -= self.action_time
            self.num_cargo += 1
            field.collect_cargo(self.selected_cargo)
            self.__next_action()

        return dt

    def shoot_ball(self, field: Field, dt: float):
        if not self.action_time:
            self.action_time = self.shoot_time
        if dt < self.action_time:
            self.action_time -= dt
        elif dt >= self.action_time:
            self.action_time = 0
            dt -= self.action_time
            self.num_cargo -= 1
            if random() <= self.accuracy:
                field.shoot_cargo(self.alliance)
            else:
                field.miss_cargo(self.alliance)
            self.__next_action()

        return dt

    def drive(self, field: Field, dt: float):
        remaining_dt = self.path.traverse(self.velocity, dt)
        self.position = self.path.position
        if self.path.done:
            self.__next_action()
            self.path = None
        return dt - remaining_dt

    def select_cargo(self, field: Field, dt: float):
        self.selected_cargo = field.select_nearest_cargo(self.alliance, self.position)
        self.path = plan_path(self.position, (self.selected_cargo.x, self.selected_cargo.y))
        self.__next_action()
        return 0.0

    def draw(self, graphics: GraphicsArea):
        graphics.draw_rect(get_alliance_color(self.alliance),
                           (self.position[0]-self.ROBOT_LEN/2, self.position[1]-self.ROBOT_LEN/2,
                            self.ROBOT_LEN, self.ROBOT_LEN))
        if self.num_cargo:
            graphics.draw_circle("black", (self.position[0], self.position[1]), Cargo.CARGO_RADIUS, 1)
        if self.path:
            self.path.draw(graphics)

    def __get_current_action(self) -> Callable:
        return self.cycle[self.current_action]

    def __next_action(self):
        self.current_action += 1
        self.current_action %= len(self.cycle)


class Line:
    def __init__(self, a: Tuple[float, float], b: Tuple[float, float]):
        self.a = a
        self.b = b
        self.m = (a[1] - b[1]) / (a[0] - b[0])

    def get_point_y(self, x: float):
        return self.m * (x - self.a[0]) + self.a[1]

    def get_point_x(self, y: float):
        return (y - self.a[1] + self.m * self.a[0]) / self.m

    def get_disection(self, other: Line):
        x = (self.m * self.a[0] - self.a[1] - other.m * other.a[0] + other.a[1]) / (self.m - other.m)
        return x, self.get_point_y(x)


class Path:
    def __init__(self, points: List[Tuple[float, float]]):
        self.points = points
        self.position = points[0]
        self.next_point_idx = 1
        self.done = False

    def traverse(self, velocity: float, dt: float) -> float:
        while dt > 0:
            next_point = self.points[self.next_point_idx]
            dx = next_point[0] - self.position[0]
            dy = next_point[1] - self.position[1]
            target_distance = sqrt(dx * dx + dy * dy)
            possible_distance = velocity * dt
            if possible_distance < target_distance:
                # We cannot arrive at target
                distance_proportion = possible_distance / target_distance
                self.position = (self.position[0] + dx * distance_proportion,
                                 self.position[1] + dy * distance_proportion)
                return 0.0
            self.position = next_point
            self.next_point_idx += 1
            dt -= target_distance / velocity
            if self.next_point_idx == len(self.points):
                self.done = True
                return (possible_distance - target_distance) / velocity

        return 0.0

    def draw(self, graphics: GraphicsArea):
        for i in range(len(self.points) - 1):
            graphics.draw_line("green", self.points[i], self.points[i+1], 5)


def get_collisions_with_rect(line: Line, top_left: Tuple[float, float], bottom_right: Tuple[float, float]):
    if (line.a[0] < top_left[0] and line.b[0] < top_left[0]) or \
            (line.a[0] > bottom_right[0] and line.b[0] > bottom_right[0]):
        return None, None, None, None
    if (line.a[1] < bottom_right[1] and line.b[1] < bottom_right[1]) or \
            (line.a[1] > top_left[1] and line.b[1] > top_left[1]):
        return None, None, None, None

    left = line.get_point_y(top_left[0])
    right = line.get_point_y(bottom_right[0])
    top = line.get_point_x(top_left[1])
    bottom = line.get_point_x(bottom_right[1])

    if not (bottom_right[1] < left < top_left[1]):
        left = None
    if not (bottom_right[1] < right < top_left[1]):
        right = None
    if not (top_left[0] < top < bottom_right[0]):
        top = None
    if not (top_left[0] < bottom < bottom_right[0]):
        bottom = None

    return left, right, top, bottom


def get_traversal_points(line: Line, top_left: Tuple[float, float], bottom_right: Tuple[float, float]):
    left, right, top, bottom = get_collisions_with_rect(line, top_left, bottom_right)
    if not left and not right and not top and not bottom:
        return ()
    # First handle adjacent sides
    if left and top:
        return top_left,
    if top and right:
        return (bottom_right[0], top_left[1]),
    if right and bottom:
        return bottom_right,
    if bottom and left:
        return (top_left[0], bottom_right[1]),

    # Now we handle opposite sides
    if left and right:
        avg = (left + right) / 2
        if (avg - bottom_right[1]) / (top_left[1] - bottom_right[1]) > 0.5:
            return top_left, (bottom_right[0], top_left[1])
        return (top_left[0], bottom_right[1]), bottom_right
    if top and bottom:
        avg = (top + bottom) / 2
        if (avg - top_left[0]) / (bottom_right[0] - top_left[0]) > 0.5:
            return (bottom_right[0], top_left[1]), bottom_right
        return top_left, (top_left[0], bottom_right[1])

    print("SHOULD NOT HAPPEN")


def plan_path(a: Tuple[float, float], b: Tuple[float, float]):
    path_points = [a]

    buffer = Robot.ROBOT_LEN / 2
    hub_top_left = (Hub.HUB_TOP_LEFT[0], Hub.HUB_TOP_LEFT[1] + Hub.HUB_DIMENSION) # This is idiotic and needs to be fixed
    obstacle_top_left = (hub_top_left[0] - buffer, hub_top_left[1] + buffer)
    obstacle_bottom_right = (hub_top_left[0] + Hub.HUB_DIMENSION + buffer,
                             hub_top_left[1] - Hub.HUB_DIMENSION - buffer)
    points = get_traversal_points(Line(a, b), obstacle_top_left, obstacle_bottom_right)
    if len(points) > 1:
        path_points.append(Line(a, points[0]).get_disection(Line(points[1], b)))
    else:
        path_points += points
    path_points.append(b)
    return Path(path_points)


