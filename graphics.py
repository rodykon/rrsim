from __future__ import annotations
import pygame
from typing import Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from pygame.surface import Surface


class GraphicsArea:

    def __init__(self, screen: Surface, top_left: Tuple[int, int], pixel_width: int, pixel_height: int,
                 real_width: float = None, real_height: float = None):
        self.screen = screen
        self.top_left = top_left
        self.width = pixel_width
        self.real_width = real_width if real_width else pixel_width
        self.height = pixel_height
        self.real_height = real_height if real_height else pixel_height

    def draw_circle(self, color, center, radius, width=0):
        if center[0] > self.width or center[1] > self.height:
            raise ValueError("Invalid circle coordinate")

        pygame.draw.circle(self.screen, color, self.__convert_point(center), radius, width)

    def draw_rect(self, color, rect):
        left, top, width, height = rect
        if left > self.width or top > self.height:
            raise ValueError("Invalid rectangle coordinate")
        new_left, new_top = self.__convert_point((left, top))
        new_width, new_height = self.__convert_dimensions(width, height)

        pygame.draw.rect(self.screen, color, (new_left, new_top-new_height, new_width, new_height))

    def fill(self, color):
        pygame.draw.rect(self.screen, color, (self.top_left[0], self.top_left[1], self.width, self.height))

    def draw_text(self, text: str, pos, size, color):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        self.screen.blit(font.render(text, True, color), self.__convert_point(pos))

    def __convert_point(self, point):
        x, y = point
        x = (x / self.real_width) * self.width
        y = (y / self.real_height) * self.height
        return int(self.top_left[0] + x), int(self.top_left[1] + (self.height - y))

    def __convert_dimensions(self, width, height):
        return int((width / self.real_width) * self.width), int((height / self.real_height) * self.height)
