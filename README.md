# Maze_Runner_UI
A cheap and cheerful top layer of code to display and debug the Maze runner work.

Requires:
- Maze module
- Runner module (does not have to be complete)
  -> If there is no "create_runner" or "explore" function, it will ignore creating a runner.
- maze_runner module
  -> There *must* already be a maze_reader function
  -> If there is a "shortest_path" function, once the runner has completed the maze, it will display it.


  How to use
  called via terminal

  Arguments
  - maze -> path to the given maze. It will load and display the maze given the instruction set passed. It interprets a maze in the *completed* format and will not do it for you.
 
  Options
  - -s | --runner int[0->2], changes the default runner, 0 is a Mouse, 1 is a Wolf, 2 is Bugbin.
  - -s | --speed int, changes the speed the runner moves at, smaller the number, faster the runner, it isn't accurate to the second, but it's close!
  - -l | --live, toggles from retracing a solved maze to attempting to render the runner in real-time. If you find your runner is stuck and unable to complete, this will allow you to view what is happening in real time. It attempts to leave a trail behind itself
  - -g | --goal x y, lets you place a non-default goal.
