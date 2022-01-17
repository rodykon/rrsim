import json
from alliance import Alliance
from robot import Robot
from field import Field
from game import ScoreBoard


class ConfigParsingException(Exception):
    pass


def safe_dict_lookup(dictionary: dict, key: str):
    if key not in dictionary:
        raise ConfigParsingException(f"Configuration file does not contain '{key}' key")
    return dictionary[key]


def parse_config(config_path: str):
    with open(config_path, "r") as config_file:
        data = json.load(config_file)

    # Robots
    robots = []
    for robot in safe_dict_lookup(data, "robots"):
        starting_pos = safe_dict_lookup(robot, "starting_position")
        starting_pos = (float(starting_pos[0]), float(starting_pos[1]))
        collect_time = float(safe_dict_lookup(robot, "collect_time"))
        shoot_time = float(safe_dict_lookup(robot, "shoot_time"))
        velocity = float(safe_dict_lookup(robot, "velocity"))
        accuracy = float(safe_dict_lookup(robot, "accuracy"))
        alliance = safe_dict_lookup(robot, "alliance")
        if alliance not in ["RED", "BLUE"]:
            raise ConfigParsingException("Alliance value must be either 'RED' or 'BLUE'")
        alliance = Alliance(alliance)
        robots.append(Robot(starting_pos, collect_time, shoot_time, velocity, accuracy, alliance))

    field_config = safe_dict_lookup(data, "field")
    field = Field(ScoreBoard(), float(safe_dict_lookup(field_config, "cargo_hub_timeout")))

    return field, robots


if __name__ == '__main__':
    parse_config("default_configs/config.json")
