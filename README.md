# Combinatorial Optimization Project

Instances are stored in the *Instances* directory. 
The bp.py is in the same directory as the instances. This file resolves the bin packing problem on the different instances.

An instance is a problem of bin packing, there is a number of products (from 20 to 150 so far) with their corresponding size and a capacity for the boxes (which 150 for each so far).

2 files will appear after the script run:

- result.txt -> contains the result of the instance in a python dataframe, saying the file instance name, the capacity of the boxes (c), the number of products (n), the physical minimum number of boxes to use (lb), the solution found by the script (in 10 max minutes), the result (success or fail) and the time of the solve
- details.txt -> contains more details about the solution, for each instance, it says which product are in which box
