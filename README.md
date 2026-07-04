# Airplane Simulation
Simple aero model of the Navion airplane solved with home brew six degree of freedom (6-DOF) solver.
Everything is written in pure Python. Minor dependance on Pygame.

## Theory of operation
In the future.

## Why?
1. To be an interactive tool and support tutorials.
2. To interact with the controller during development (Software In The Loop). This eliminates the needs for any hardware during early stages of controller develop.

## What does it simulate / demonstrate
- Linear aerodinamics with secondary effects.
- Movement in 3D space.
- Support four views (chase, pilot, follow and static).
- Animation of gears, engine plume and weight on wheels.

### Take off in real-time and 3D wireframe graphics.
![alt text](./figures/takeoff_20fps.gif "")

## Known issues.
- 6DOF attitude will crash if calculated with time intervals larger than 10 ms (that is a numerical limitation).
- The 3D wireframe engine has bug when drawing ling that start and end before and after the viewer.

## Future plans.
- Demonstrate closed-loop controlers.

Requires Python to run the example code (inclues dedicated unit-test). For visual support install pyGame and GSOF_3dWireFrame.

http://python.org/

http://www.pygame.org

https://github.com/mrGSOF/3dWireFrame

or

https://github.com/mrGSOF/GSOF_3dWireFrame

## Running instructions
- Install requirements `pip install -r requirements.txt`
- or run `pip install GSOF_3dWireFrame`
- Clone and install GSOF_Cockpit (`pip install .` or `setup.bat`)
- Clone flightSim
- run `python Simulation.py`

Interactive operation is supported using the mouse and keyboard.
Press 'Q' and 'A' to increase and decrease throttle
Press 'G' and 'B' to retract and extend landing gears
Press 'Z' and 'C' to trim rudder, 'X' to reset
Press '1' to '3' to select point of view
