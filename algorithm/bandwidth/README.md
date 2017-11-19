# Sync and mobility IoT

## Problem
Write a program that computes the bandwidth between 2 given machines in a
mobility IoT network, given the individual bandwidths of all the connections
in the network. In this problem, assume that the bandwidth of a connection is
always the same in both directions (which is not necessarily true in the real
world).

## Input
The input file contains description of several networks.

### First line
Every description starts with a line containing a single integer n (2 <= n <= 100), which is the
number of machines in the network. The machines are numbered from 1 to n.

### Second line
The next line contains 3 numbers s, d, and c. The numbers s and d are the source and
destination machines, and the number c is the total number of connections in the
network.

### Other lines
Following this are c lines describing the connections.
Each of the c lines contains 3 integers: the first 2 are the numbers of the
connected machines, and the 3rd number is the bandwidth of the connection. The
bandwidth is a non-negative number not greater than 1000.

### Misc.
There might be more than one connection between a pair of machines, but a
machine cannot be connected to itself. All connections are bi-directional, i.e.
data can be transmitted in both directions along a connection, but the sum of
the amount of data transmitted in both directions must be less than the
bandwidth. A line containing the number 0 follows the last network description,
and terminates the input.

## Output
For each network description, first print the number of the network. Then print
the total bandwidth between the source machine s and the destination machine d,
following the format of the sample output. Print a blank line after each test
case.
