from __future__ import annotations
from math import exp, log
from random import random
import numpy as np
from math import ceil
import csv
from typing import List
from alliance import Alliance, get_alliance_color
import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graphics import GraphicsArea

NUM_CARGO = 11
FIELD_WIDTH = 16.46
FIELD_HEIGHT = 8.23
HUB_WIDTH = 2.72
HUB_BOTTOM = (FIELD_WIDTH/2.0-HUB_WIDTH/2.0, FIELD_HEIGHT/2.0-HUB_WIDTH/2.0)
HUB_TOP = (FIELD_WIDTH/2.0+HUB_WIDTH/2.0, FIELD_HEIGHT/2.0+HUB_WIDTH/2.0)
C_BOTTOM = - 0.01
C_TOP = FIELD_HEIGHT + 0.01
C_LEFT = - 0.1
C_RIGHT = FIELD_WIDTH + 0.1
DIST_HEIGHT = 9
DIST_WIDTH = 17


DISTRIBUTION_PATH = "default_configs/cargo_dist.csv"


class Cargo:
    CARGO_RADIUS = 0.24

    def __init__(self, x: float, y: float, alliance: Alliance):
        self.x = x
        self.y = y
        self.alliance = alliance
        self.is_selected = False

    def __str__(self):
        return f"Cargo({self.x}, {self.y}, {self.alliance})"

    def __repr__(self):
        return f"Cargo({self.x}, {self.y}, {self.alliance})"

    def draw(self, graphics: GraphicsArea):
        graphics.draw_circle(get_alliance_color(self.alliance), (self.x, self.y), self.CARGO_RADIUS)


def y_func(r: float) -> float:
    if r <= 0.5:  # Field top
        b = (log(C_TOP - HUB_TOP[1]) - log(C_TOP - FIELD_HEIGHT)) / (0.5 - 0)
        a = exp(log(C_TOP - HUB_TOP[1]) + b * 0)
        b = -b
        c = C_TOP
    else:  # Field bottom
        b = (log(HUB_BOTTOM[1] - C_BOTTOM) - log(0 - C_BOTTOM)) / (1.0 - 0.5)
        a = exp(log(HUB_BOTTOM[1] - C_BOTTOM) - b * 1.0)
        a = -a
        c = C_BOTTOM
    return c - a * exp(b * r)


def x_func(r: float) -> float:
    if r <= 0.5:  # Field right
        b = (log(C_RIGHT - HUB_TOP[0]) - log(C_RIGHT - FIELD_WIDTH)) / (0.5 - 0)
        a = exp(log(C_RIGHT - HUB_TOP[0]) + b * 0)
        b = -b
        c = C_RIGHT
    else:  # Field left
        b = (log(HUB_BOTTOM[0] - C_LEFT) - log(0 - C_LEFT)) / (1.0 - 0.5)
        a = exp(log(HUB_BOTTOM[0] - C_LEFT) - b * 1.0)
        a = -a
        c = C_LEFT
    return c - a * exp(b * r)


def gen_coord_array():
    return [val for val in range(ceil(FIELD_WIDTH)*ceil(FIELD_HEIGHT))]


def get_cargo_dist():
    raw_vals = []
    with open(DISTRIBUTION_PATH, "r") as dist_file:
        reader = csv.reader(dist_file)
        for row in reader:
            for val in row:
                raw_vals.append(int(val))
    arr = np.array(raw_vals)
    normalized = (arr - arr.min()) / (arr.max() - arr.min())
    return normalized / normalized.sum()


def get_random_cargo(alliance: Alliance) -> Cargo:
    sample_index = np.random.choice(gen_coord_array(), p=get_cargo_dist())
    block_y, block_x = np.unravel_index(sample_index, (ceil(FIELD_HEIGHT), ceil(FIELD_WIDTH)))

    block_width = FIELD_WIDTH / DIST_WIDTH
    block_height = FIELD_HEIGHT / DIST_HEIGHT

    real_x = block_width * block_x + random() * block_width
    real_y = block_height * block_y + random() * block_height
    return Cargo(real_x, real_y, alliance)


def initialize_cargo() -> List[Cargo]:
    return [get_random_cargo(Alliance.RED) for _ in range(NUM_CARGO)] + \
           [get_random_cargo(Alliance.BLUE) for _ in range(NUM_CARGO)]
    