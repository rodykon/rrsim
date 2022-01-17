from argparse import ArgumentParser
import pygame
import time
from pygame.locals import *
from graphics import GraphicsArea
from cargo import FIELD_WIDTH, FIELD_HEIGHT
from config import parse_config
import sys

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


def parse_args():
    parser = ArgumentParser("RRSIM - FRC 2022 Rapid React Simulator")
    parser.add_argument("config_file", nargs="?", default="default_configs/config.json",
                        help="Path to the JSON configuration file.")
    return parser.parse_args()


def main():
    field, bots = parse_config(parse_args().config_file)
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

    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()


if __name__ == '__main__':
    main()
