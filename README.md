# py-rubik_solver
## Python solver for a rubik's cube
This program makes a 3D representation of a rubiks cube and solves it step by step.
## Usage
To use this program you need to execute the following commands
- For 3D visualizations:


    ```python visualizer.py```
- For statistics:


    ```python stats.py```
## Requirements
To use this program you need to install _python 3.8.10_ or later (although it will probably work on _python 3.7_)
You will also need a recent version of _numpy_ and _vpython 7_ or later, those can be installed with:

```pip install numpy vpython```

## Implementation
This project is separated in different files, each implementing a different functionality. The content and functionality of each of these files is the following:
### configs.py
This file contains general configuration parameters mostly related to the visual representation of the cube:
- The default colors
- The number of fps
- The time taken to reproduce each move
- Time to wait between moves
- Speed factor
### cube.py
This file contains the ```Cube``` class, which implements a data structure for storing the pieces of the cube and some functions for rotating the faces of the cube. It also implements the possibility to shuffle the cube on creation and the possibility of recording a list of moves made in the cube, this is used for generating a solution.

The main functions implemented in this class are:
- ```move(move, n=1, record=True)```: where _move_ should be a string representing the face to move and _n_ is the number of 90 degree rotations to perform (2 is half turn and 3 or -1 is a turn to the other side). The codes used for the _move_ are:
    - _"U", "F", "R", "B", "L", "D"_ for individual faces.
    - _"UD", "FB", "RL"_ for the middle faces.
    - _"UU", "FF", "RR"_ for rotations of the whole cube along this axis.
    
- ```rotate(axis, n=1)```: this has the same effect as using ```move``` with _"UU", "FF", "RR"_ but these moves are never recorded.
- ```is_solved()```: checks whether the cube equals the solved cube. Keep in mind that this function will return ```False``` even if the cube is solved but faces a different way.
- ```copy()```: creates a _deep_copy_ of the cube. The copy is completely independent of the original cube.
### cube_3d.py
This file implements the ```Cube3D``` class, which directly inherits from the ```Cube``` class. This class overrides the ```__init__``` and ```move``` functions to first create all the cubes necessary to represent the rubiks cube in 3D and then animate them each time any face is moved.
### cube_solver.py
This file implements the ```CubeSolver``` class, which acts as an abstract class for all the other solving algorithms. It only takes care of taking some measures for statistics.
### simple_solver.py
This is the first solving algorithm implemented, it's the usual _beginer_ algorithm for anyone learning how to solve the rubiks cube. It's implemented on a really naive way, and it's far from optimal in terms of the number of steps of the solution. It was just a proof of concept and my goal is to implement a better, more efficient version of this class in the future.

In my personal computer this algorithm takes ```1.78 ms``` on average to compute a solution, and the solutions have ```205.6``` steps on average. Again these results are far from good, but this was just a proof of concept.

The process of the algorithm is separated in different steps, which are:
- *solve_first_cross*: solves the cross on the _UP_ face
- *solve_first_corners*: solves the corners on the _UP_ face
- *solve_second_row*: solves the second _"crown"_ or the second row
- *solve_second_cross*: creates a cross on the _DOWN_ face
- *orientate_2nd_cross*: positions correctly the pieces inside the cross on the _DOWN_ face
- *solve_second_corners*: positions correctly the corners in the _DOWN_ face
- *orientate_2nd_corners*: rotates correctly the corners in the _DOWN_ face
- *reorient_cube*: rotates the whole cube so that the _UP_ face is facing up and the _FRONT_ face if facing front
### stats.py
This file is used to compute some statistics of the cube solutions. At this point this file is used to compute:
- The average _time_ taken to generate a solution
- The average _number of steps_ of the generated solutions
- Some data of the solving process

Keep in mind the data computed will probably change in the future.
### util.py
In this file we store different _lists_ and _dictionaries_ used in the project such as a solved cube structure, a list of the directions, a _function_ for generating random moves, ...
### visualizer.py
This file is used to launch a 3D representation of the solving process of the cube. It also contains a function to check the progress of the solving algorithm.
## Notes
In the future I'm planing to make **more solving algorithms** as well as an implementation for a **physical robot** that solves a given cube.

Use this code as you wish, just let me know if you do, **I'll love to hear what you are up to!**

If you have any _doubts/comments/suggestions/anything_ please let my know via email at ```polqb2000@gmail.com``` or at the email in my profile.
