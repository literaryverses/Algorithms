# Algorithms
A collection of personal projects to explore some algorithms in python. Within each folder is a topic which contains the code and a textfile for references.

## Table of contents
1. [Floorplans](#floorplans)

## Floorplans <a name="floorplans"></a>
In electronic design automation, a floorplan of an integrated circuit is a schematics representation of tentative placement of its major functional blocks. Here, I look into mathematical models to generate the optimal floorplan.

### internalAR.py
Returns iterations of a binary tree based on *n* internal nodes via recursion. The iterations are provided as array representation: the top row represents the left subtrees, the bottom row represents the right subtrees, and each column represents an internal node in order of preorder traversal.

### skarbek.py
Performs the same operation as internalAR.py, but uses Skarbek's Algorithm instead. The algorithm is nonrecursive and its runtime per tree is O(1). References are provided in floorplans/resources.txt

### expandFP.py
Slicing floorplans can be represented by Polish Expressions. Given a set of dimensions and a Polish Expression, this program caculates the overall height and width of the floorplan.