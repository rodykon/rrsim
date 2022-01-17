from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Callable
from alliance import get_alliance_color
from cargo import Cargo
from math import sqrt
if TYPE_CHECKING:
    from field import Field
    from alliance import Alliance
    from graphics import GraphicsArea


class Robot:
    ROBOT_LEN = 0.7

    def __init__(self, position: Tuple[float, float], collect_time: float, shoot_time: float, velocity: float,
                 alliance: Alliance):
        self.position = position
        self.collect_time = collect_time
        self.shoot_time = shoot_time
        self.velocity = velocity
        self.alliance = alliance
        self.num_cargo = 0

        self.action_time = 0.0
        self.current_action = 0
        self.post_action_time = 0.0
        self.selected_cargo = None
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
            field.shoot_cargo(self.alliance)
            self.__next_action()

        return dt

    def drive(self, field: Field, dt: float):
        dx = self.selected_cargo.x - self.position[0]
        dy = self.selected_cargo.y - self.position[1]
        target_distance = sqrt(dx*dx + dy*dy)
        possible_distance = self.velocity * dt
        if possible_distance >= target_distance:  # We can arrive at target
            self.__next_action()
            self.position = (self.selected_cargo.x, self.selected_cargo.y)
            return (possible_distance - target_distance) / self.velocity
        # We cannot arrive at target
        distance_proportion = possible_distance / target_distance
        self.position = (self.position[0] + dx * distance_proportion, self.position[1] + dy * distance_proportion)
        return dt

    def select_cargo(self, field: Field, dt: float):
        self.selected_cargo = field.select_nearest_cargo(self.alliance, self.position)
        self.__next_action()
        return 0.0

    def draw(self, graphics: GraphicsArea):
        graphics.draw_rect(get_alliance_color(self.alliance),
                           (self.position[0]-self.ROBOT_LEN/2, self.position[1]-self.ROBOT_LEN/2,
                            self.ROBOT_LEN, self.ROBOT_LEN))
        if self.num_cargo:
            graphics.draw_circle("black", (self.position[0], self.position[1]), Cargo.CARGO_RADIUS, 1)

    def __get_current_action(self) -> Callable:
        return self.cycle[self.current_action]

    def __next_action(self):
        self.current_action += 1
        self.current_action %= len(self.cycle)
