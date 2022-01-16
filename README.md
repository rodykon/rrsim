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
