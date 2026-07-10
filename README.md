# Airplane Simulation
Simple aero model of the Navion airplane solved with homebrew six degree of freedom (6-DOF) solver.
Complete Python code of the aerodynamic model, 6DOF solver, math library and 2D/3D visualisation.
Minor dependancy on Pygame or ptgame-ce.

## Theory of operation
In the future.

## Why?
1. To be an interactive tool for learning and experimenting.
2. To interact with a closed-loop controller during development (Software In The Loop). This eliminates the needs for any hardware during early stages of controller develop.
3. Complete and exposed code that the user can learn and modify. 

## What does it simulate / demonstrate
- Linear aerodinamics with secondary effects.
- Movement in 3D space.
- Collision detection with ground.
- 3D wireframe graphics with five views (chase, pilot, follow, above and static).
- Animation of gears, engine plume and weight on wheels.

### Take off in real-time and 3D wireframe graphics.
![alt text](./figures/takeoff_20fps.gif "")

## Known issues.
- 6DOF attitude will crash if calculated with time intervals larger than 10 ms (that is a numerical limitation).
- Not simulating gyroscopic effects (for know).

## Future plans.
- Demonstrate closed-loop controlers.
- Add gyroscopic effects.
- Add support for real time telemetry over UDP.

## Running instructions
Install Python from `http://python.org/`. Tested with versions 3.10 to 3.14.
- Install requirements `pip install -r requirements.txt`
- run `pip install pygame-ce` or `pip install pygame`
- run `pip install GSOF_3dWireFrame`
- run `pip install GSOF_Cockpit`
- Clone flightSim
- run `python Simulation.py`

Interactive operation is supported using the mouse and keyboard.
Press 'Q' and 'A' to increase and decrease throttle
Press 'G' and 'B' to retract and extend landing gears
Press 'Z' and 'C' to trim rudder, 'X' to zero
Press '1' to '5' to select point of view
