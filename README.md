# Algorithms
A collection of personal projects to explore some algorithms in python. Within each folder is a topic which contains the code and a textfile for references.

## Table of contents
1. [Sorting](#sorting)
2. [Maze generation](#maze_generation)
3. [Floorplans](#floorplans)


## Sorting <a name="sorting"></a>
Sorting is an operation that puts elements of an array into an order, most frequently numerical or lexicographical. Here, I explore different types of sorting algorithms and their methods.

### bubblesort.py
Bubble sort is simplest and most impractical sorting algorithm that swaps out adjacent elements if they are in the wrong order, with a runtime of O(n<sup>2</sup>). Variants of bubble sorting is explored, such as modified bubble sort (which quits when no swaps are made) and cocktail shaker sort (bidirectional bubble sort).

### insertsort.py
Insertion sort partitions an array and then inserts elements from the unsorted section to the sorted one. Variants of this algorithm uses two-way insertion or binary insertion

## Maze Generation <a name="maze_generation"></a>
Maze generation algorithms use automated methods to create mazes.

### objects.py
Creating data structures via cell and grid classes

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