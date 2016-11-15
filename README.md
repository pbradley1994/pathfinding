# Interactive Pathfinding Desktop App

An interactive tool for exploring pathfinding algorithms on a 2D grid. Modify the kind of algorithm and the state of the map.

![GIF](/Screenshots/AStar3.gif)

## Algorithms
Currently comes with 7 pathfinding algorithms:
 - Breadth First Search
 - Dijkstra's Algorithm
 - Greedy Best-First Search
 - A*
 - Dynamic Weight A*
 - Bidirectional Retargeting Search
 - Theta*

## Executable
An executable version (for Windows) of this code can be downloaded at:
 - https://www.mediafire.com/?7toag7t9an9ntkw

## Default Controls:

Use your mouse.

Select 'Show Arrows' to have each node point to its parent.

Select 'Show Costs' to show the cumulated cost of each node.

Select the dropdown menu to change the algorithm used.

Click on a node to have it cycle through a cost of 1, a cost of 5, and totally impassable.

### Prerequisites

To run this, you will need to download and install the following:

* [Python 2.7.x+](https://www.python.org/downloads/release/python-2712/) - Python 3.x may not work
* [Pygame 1.9.1+](http://www.pygame.org/download.shtml) - The framework used to handle rendering and sound

### Possible Improvements

 - Add ability to click and hold to change node state en masse.
 - Allow dynamic change of size of graph.
 - Add ability to rewind, go one step through, etc.

### More Screenshots
![FirstScreen](/Screenshots/FirstScreen)
![BFS1](/Screenshots/BFS1.png) 
![BFS2](/Screenshots/BFS2.png)
![Greedy](/Screenshots/Greedy1.png)
![Djikstra](/Screenshots/Djikstra1.png)
![AStar](/Screenshots/Astar1.png) 
![Theta](/Screenshots/Theta1.png)