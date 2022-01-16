from robot import Robot
from game import ScoreBoard
from alliance import Alliance
from field import Field
import pygame
import time
from pygame.locals import *
from graphics import GraphicsArea
from cargo import FIELD_WIDTH, FIELD_HEIGHT
from config import parse_config
import sys

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


def main():
    # Initialize robots
    field, bots = parse_config("default_configs/config.json")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Rapid React Simulator')
    field_area = GraphicsArea(screen, (0, 0), SCREEN_WIDTH, SCREEN_WIDTH//2, FIELD_WIDTH, FIELD_HEIGHT)
    score_area = GraphicsArea(screen, (0, SCREEN_WIDTH//2), SCREEN_WIDTH, SCREEN_HEIGHT-SCREEN_WIDTH//2)
    total_time = 0.0
    last_time = time.time()
    while total_time < 60.0 * 2.0:
        current_time = time.time()
        dt = current_time - last_time
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()
        for bot in bots:
            bot.perform_actions(field, dt)
        field.update_field(dt)
        field.score_keeper.update(dt)

        field_area.fill("white")
        field.draw(field_area)
        for bot in bots:
            bot.draw(field_area)
        field.score_keeper.draw(score_area)
        pygame.display.flip()
        total_time += dt
        last_time = current_time


if __name__ == '__main__':
    main()
