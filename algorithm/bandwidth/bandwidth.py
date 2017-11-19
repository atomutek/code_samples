#!/usr/bin/env python

'''
    File name: bandwidth.py
    Python Version: 2.7
    Description: Bandwidth for IoT
'''

__author__ = "Matthieu Destephe"
__email__ = "matt@atomutek.org"

import sys
from Graph import Graph


if __name__ == "__main__":

    if len(sys.argv) is not 2:
        print "Wrong numbers of parameters"
        print "python bandwidth.py file_to_input"
        sys.exit(1)

    network_index = 1

    new_network = True

    with open(sys.argv[1], 'rb') as input_file:
        for line in input_file:
            # Get first line
            first_line = line.rstrip().split(' ')
            nb_of_machines = int(first_line[0])

            if nb_of_machines == 0:
                break

            # init graph
            graph = [[0 for x in xrange(100)] for y in xrange(100)]
            g = Graph(graph)

            # Get the second line
            second_line = next(input_file).rstrip().split(' ')
            source = int(second_line[0])
            sink = int(second_line[1])
            nb_connections = int(second_line[2])

            # Get the connections
            for _ in xrange(nb_connections):
                connection = next(input_file).rstrip().split(' ')
                machine_a = int(connection[0])
                machine_b = int(connection[1])
                bandwidth = int(connection[2])

                if graph[machine_a][machine_b] == 0:
                    graph[machine_a][machine_b] = bandwidth
                if graph[machine_b][machine_a] == 0:
                    graph[machine_b][machine_a] = bandwidth

            print "Network %d" % network_index
            print "The bandwidth is %d.\n" % g.EdmondsKarp(source, sink)
            network_index += 1
