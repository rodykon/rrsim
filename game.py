from __future__ import annotations
from alliance import Alliance, get_alliance_color
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graphics import GraphicsArea


class ScoreBoard:
    def __init__(self):
        self.score = {Alliance.RED: 0, Alliance.BLUE: 0}
        self.time = 0.0

    def cargo_to_top(self, alliance: Alliance):
        self.score[alliance] += 2

    def update(self, dt):
        self.time += dt

    def draw(self, graphics: GraphicsArea):
        graphics.draw_rect(get_alliance_color(Alliance.BLUE), (0, 0, graphics.real_width / 3, graphics.real_height))
        graphics.draw_text(str(self.score[Alliance.BLUE]), (graphics.real_width / 6, graphics.real_height * 3/4), 40, "white")
        graphics.draw_rect("green", (graphics.real_width / 3, 0, graphics.real_width / 3,
                                      graphics.real_height))
        graphics.draw_text(str(int(self.time)), (graphics.real_width / 2, graphics.real_height * 3 / 4),
                           40, "white")
        graphics.draw_rect(get_alliance_color(Alliance.RED), (2 * graphics.real_width / 3, 0, graphics.real_width / 3,
                                                              graphics.real_height))
        graphics.draw_text(str(self.score[Alliance.RED]), (graphics.real_width * 5 / 6, graphics.real_height * 3/4), 40, "white")

