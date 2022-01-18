# rrsim
Simulator for FRC 2022 challenge: Rapid React

## Usage

In order to run the simulator use the following:

```bash
python3 rrsim.py [config_path]
```

where `config_path` is the path to the json configuration (default value is `default_configs/config.json`).

## Configurations

In order to configure game, field and robots, a config JSON file must be created. See `default_configs` directory for examples of configurations.
The following are parameters that can be defined in the configuration:

Per-robot parameters:

| Name              | Type | Meaning                       | Example|
|-------------------|------|-------------------------------|---------|
| starting_position |Tuple[float, float]| Starting position of the robot|[1.0, 2.0]|
| collect_time      |float| Time it takes the robot to collect cargo | 3.0|
| shoot_time        |float| Time it takes the robot to shoot cargo |1.0|
| velocity          |float| Drive velocity of the robot   |5.0|
| accuracy          |float| Shooting accuracy of the robot|0.95|
|  alliance         |Enum{RED,BLUE}| Alliance of the robot | RED|

Field parameters:

|Name | Type | Meaning                                  | Example|
|-----|------|------------------------------------------|---------|
|cargo_hub_timeout|float|Time it takes from the moment cargo enters the hub to the moment it is collectable on the floor|10.0|
|match_length|float|Length of the simulation|120.0|

Units for the values in the configurations can be seen in the [units](#units) section.

In addition to the configuration JSON file, a cargo distribution CSV file is required. This file is basically a matrix of integers where every integer represents the probability (relative to the other integers) that a cargo will appear in the 1x1 meter square corresponding to that number in the matrix. A default distribution is supplied in the `default_configs` directory.


## The Simulation

Once a configuration has been created (or selected) and the simulator was ran, A window will pop up which contains the actual simulator.
This window consists of two sections. In the top - the field, in which robots are represented by squares and cargo by circles.
In the bottom - the scoreboard, which is itself divided into three areas, from left to right - blue score, time since the beginning of the match, red score.


## Units

rrsim uses the following units:

Quantity       | Units
---------------|--------
Length/Distance| Meters
Time           | Seconds
Velocity       | Meters per second


## Planned Additions

* Ability to fast forward the simulation.
* Configurable cycle types for robots
  * Collect only from one side of the field
  * Play defence
  * Collect two balls at a time
  * Score to low hub
* Penalty for having many robots in the same place
  * Something like "work 10% slower for every robot in your immediate vicinity".
  
And here are some additions that are probably too overkill to bother with:

* Robot path planning
