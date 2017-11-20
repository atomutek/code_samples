# Sync and mobility IoT: Notes

There are two ways to find a solution:
- Ford-Fulkerson method
- Edmonds-Karp algorithm

Edmonds-Karp is an amelioration of Ford-Fulkerson, using Breadth Search First to
determine the search order when finding the augmenting path.

## Issues
The network 2 in the text is 28 and I found 25. It needs to be investigated.

__Solution__
- Issue was that there were 2 connections from 2 to 3 and 3 to 2
  - from the context: assume that the bandwidth of a connection is
  always the same in both directions
  - Therefore 2 (or X) bi-directional connections between 2 same machines have
  their bandwidths summed.

## Scripts
- bandwidth.py: My solution to the problem.
- network_ek.py: Another script was written based on a 3rd party module _networkx_.
  - The module seems to not handle 2+ bi-directional connections between 2 same machines though.
