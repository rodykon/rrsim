from __future__ import annotations
from alliance import Alliance, get_alliance_color
from cargo import initialize_cargo, get_random_cargo
from math import sqrt
from typing import Dict, TYPE_CHECKING
from cargo import FIELD_WIDTH, FIELD_HEIGHT, Cargo
if TYPE_CHECKING:
    from cargo import Cargo
    from game import ScoreBoard
    from graphics import GraphicsArea


class Hub:
    HUB_DIMENSION = 2.72
    HUB_TOP_LEFT = ((FIELD_WIDTH - HUB_DIMENSION) / 2, (FIELD_HEIGHT - HUB_DIMENSION) / 2)

    def __init__(self, cargo_hub_timeout: float):
        self.cargo_hub_timeout = cargo_hub_timeout
        self.cargo_timeouts = {Alliance.RED: [], Alliance.BLUE: []}

    def add_cargo(self, alliance: Alliance):
        self.cargo_timeouts[alliance].append(self.cargo_hub_timeout)

    def get_fallen_cargo(self, dt: float) -> Dict[Alliance, int]:
        return {Alliance.RED: self.__get_fallen_cargo(dt, Alliance.RED),
                Alliance.BLUE: self.__get_fallen_cargo(dt, Alliance.BLUE)}

    def __get_fallen_cargo(self, dt: float, alliance: Alliance) -> int:
        new_timeouts = []
        result = 0
        for timeout in self.cargo_timeouts[alliance]:
            timeout -= dt
            if timeout <= 0.0:
                result += 1
            else:
                new_timeouts.append(timeout)
        self.cargo_timeouts[alliance] = new_timeouts
        return result

    def draw(self, graphics: GraphicsArea):
        graphics.draw_rect("grey", (self.HUB_TOP_LEFT[0], self.HUB_TOP_LEFT[1], self.HUB_DIMENSION, self.HUB_DIMENSION))

        cursor = [self.HUB_TOP_LEFT[0] + Cargo.CARGO_RADIUS, self.HUB_TOP_LEFT[1] + Cargo.CARGO_RADIUS]
        for i in range(len(self.cargo_timeouts[Alliance.BLUE])):
            graphics.draw_circle(get_alliance_color(Alliance.BLUE), cursor, Cargo.CARGO_RADIUS)
            cursor[0] += Cargo.CARGO_RADIUS * 2
            if cursor[0] > self.HUB_TOP_LEFT[0] + self.HUB_DIMENSION / 2:
                cursor[0] = self.HUB_TOP_LEFT[0] + Cargo.CARGO_RADIUS
                cursor[1] += Cargo.CARGO_RADIUS * 2

        cursor = [self.HUB_TOP_LEFT[0] + self.HUB_DIMENSION / 2 + Cargo.CARGO_RADIUS,
                  self.HUB_TOP_LEFT[1] + Cargo.CARGO_RADIUS]
        for i in range(len(self.cargo_timeouts[Alliance.RED])):
            graphics.draw_circle(get_alliance_color(Alliance.RED), cursor, Cargo.CARGO_RADIUS)
            cursor[0] += Cargo.CARGO_RADIUS * 2
            if cursor[0] > self.HUB_TOP_LEFT[0] + self.HUB_DIMENSION:
                cursor[0] = self.HUB_TOP_LEFT[0] + self.HUB_DIMENSION / 2 + Cargo.CARGO_RADIUS
                cursor[1] += Cargo.CARGO_RADIUS * 2


class Field:
    def __init__(self, score_keeper: ScoreBoard, cargo_hub_timeout: float):
        self.floor_cargo = initialize_cargo()
        self.selected_cargo = []
        self.score_keeper = score_keeper
        self.hub = Hub(cargo_hub_timeout)

    def update_field(self, dt):
        for alliance, fallen_cargo in self.hub.get_fallen_cargo(dt).items():
            for _ in range(fallen_cargo):
                self.floor_cargo.append(get_random_cargo(alliance))

    def shoot_cargo(self, alliance: Alliance):
        self.hub.add_cargo(alliance)
        self.score_keeper.cargo_to_top(alliance)

    def miss_cargo(self, alliance: Alliance):
        self.floor_cargo.append(get_random_cargo(alliance))

    def select_nearest_cargo(self, alliance: Alliance, position) -> Cargo:
        chosen = min([cargo for cargo in self.floor_cargo if cargo.alliance == alliance and not cargo.is_selected],
                     key=lambda cargo: sqrt((cargo.x-position[0])**2 + (cargo.y-position[1])**2))
        chosen.is_selected = True
        return chosen

    def collect_cargo(self, to_collect: Cargo):
        self.floor_cargo.remove(to_collect)

    def draw(self, graphics: GraphicsArea):
        for cargo in self.floor_cargo:
            cargo.draw(graphics)
        self.hub.draw(graphics)
