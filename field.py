from __future__ import annotations
from alliance import Alliance
from cargo import initialize_cargo, get_random_cargo
from math import sqrt
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from cargo import Cargo
    from game import ScoreBoard
    from graphics import GraphicsArea


class Field:
    def __init__(self, score_keeper: ScoreBoard, cargo_hub_timeout: float):
        self.floor_cargo = initialize_cargo()
        self.basket_balls = {Alliance.RED: 0, Alliance.BLUE: 0}
        self.curr_time = 0.0
        self.basket_timeouts = {Alliance.RED: [], Alliance.BLUE: []}
        self.selected_cargo = []
        self.score_keeper = score_keeper
        self.cargo_hub_timeout = cargo_hub_timeout

    def update_field(self, dt):
        self.__update_basket_balls(Alliance.RED, dt)
        self.__update_basket_balls(Alliance.BLUE, dt)

    def __update_basket_balls(self, alliance: Alliance, dt: float):
        new_timeouts = []
        for timeout in self.basket_timeouts[alliance]:
            timeout -= dt
            if timeout <= 0.0:
                self.basket_balls[alliance] -= 1
                self.floor_cargo.append(get_random_cargo(alliance))
            else:
                new_timeouts.append(timeout)
        self.basket_timeouts[alliance] = new_timeouts

    def shoot_cargo(self, alliance: Alliance):
        self.basket_balls[alliance] += 1
        self.basket_timeouts[alliance].append(self.cargo_hub_timeout)
        self.score_keeper.cargo_to_top(alliance)

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
