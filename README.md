# Algorithms
A collection of personal projects to explore some algorithms in python. Within each folder is a topic which contains the code and a textfile for references.

## Table of contents
1. [Sorting](#sorting)
2. [Maze](#maze)
3. [Floorplans](#floorplans)
4. [Color](#color)


## Sorting <a name="sorting"></a>
Sorting is an operation that puts elements of an array into an order, most frequently numerical or lexicographical.

### bubblesort.py
Bubble sort is simplest and most impractical sorting algorithm that swaps out adjacent elements if they are in the wrong order, with a runtime of O(n<sup>2</sup>). Variants of bubble sorting is explored, such as modified bubble sort (which quits when no swaps are made) and cocktail shaker sort (bidirectional bubble sort).

### insertsort.py
Insertion sort partitions an array and then inserts elements from the unsorted section to the sorted one. Variants of this algorithm uses bidirectional insertion or binary search insertion.


## Maze <a name="maze"></a>
Algorithms that work with mazes: automatic generation and (eventually) pathfinding

### alphabet.py
Takes inputs from a string to generate a template of an orthogonal maze with words within them.

### maze_generation.py
Algorithms that randomly and automatically generate mazes

### maze_solving.py
Algorithms that solve mazes. Categorized as inside (can be implemented within a cell), outside (needs the entire layout), and other (miscellaneous implementations that can belong two either of the two groups but are special in their own way)

### objects.py
Creates data structures via cell and grid classes to serve as the foundation of several types of mazes such as orthogonal (4-sided cells), delta (3-sided cells), and sigma (6-sided cells). Other features include masking (selectively removing a cell from being involved with a maze), braiding (preventing mazes from having dead ends), and stacking (building adding multiple layers on top of a maze)


## Floorplans <a name="floorplans"></a>
In electronic design automation, a floorplan of an integrated circuit is a schematics representation of tentative placement of its major functional blocks. Here, I look into mathematical models to generate the optimal floorplan.

### internalAR.py
Returns iterations of a binary tree based on *n* internal nodes via recursion. The iterations are provided as array representation: the top row represents the left subtrees, the bottom row represents the right subtrees, and each column represents an internal node in order of preorder traversal.

### skarbek.py
Performs the same operation as internalAR.py, but uses Skarbek's Algorithm instead. The algorithm is nonrecursive and its runtime per tree is O(1). References are provided in floorplans/resources.txt

### createsFP.py
Generates the dimensions of a slicing floorplan along with its corresponding normalized Polish Expression based on the number of slices performed on the floorplan.

### expConvert.py
Translates expressions between postfix notation and infix notation using stacks and queues. Three algorithms are implemented for translating infix notation to postfix notation, among them Dijkstra's Shunting-Yard algorithm.

### expandFP.py
Slicing floorplans can be represented by Polish Expressions (postfix notation). Given a set of dimensions and a Polish Expression, this program caculates the overall height and width of the floorplan.

### orientsFP.py
Implements Stockmeyer's polynomial-time algorithm for finding optimal orientations for slicing floorplans.  Needs three inputs: a normalized Polish Expression representing the floorplan, a string of dimensions represented as '(height, width)...' and non-decreasing cost function ψ that uses h and w (representing height and width respectively) as parameters.

### optimalFP.py
Implements simulated annealing to generate optimal floorplans given a series of dimensions expressed as a Polish Expression through a stochastic process. 


## Color <a name="color"></a>
Algorithms involved with color. Primarily uses RGB to represent color.

### conversion.py
Converts between color representations into other formats of different color models.

### operations.py
Takes a RGB input and returns several color schemes