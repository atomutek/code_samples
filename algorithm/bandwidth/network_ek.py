#!/usr/bin/env python

'''
    File name: network_ek.py
    Python Version: 2.7
    Description: Bandwidth for IoT
'''

__author__ = "Matthieu Destephe"
__email__ = "matt@atomutek.org"

import sys
import networkx as nx
from networkx.algorithms.flow import edmonds_karp

if __name__ == "__main__":

    if len(sys.argv) is not 2:
        print "Wrong numbers of parameters"
        print "python network_ek.py file_to_input"
        sys.exit(1)

    network_index = 1

    with open(sys.argv[1], 'rb') as input_file:
        for line in input_file:

            # Get first line
            first_line = line.rstrip().split(' ')
            nb_of_machines = int(first_line[0])

            if nb_of_machines == 0:
                break

            # init graph
            graph = nx.DiGraph()

            # Get the second line
            second_line = next(input_file).rstrip().split(' ')
            source = second_line[0]
            sink = second_line[1]
            nb_connections = int(second_line[2])

            # Get the connections
            for _ in xrange(nb_connections):
                connection = next(input_file).rstrip().split(' ')
                machine_a = connection[0]
                machine_b = connection[1]
                bandwidth = int(connection[2])

                graph.add_edge(machine_a, machine_b, capacity=bandwidth)

            print "Network %d" % network_index
            ek = edmonds_karp(graph, source, sink)
            print "The bandwidth is %d.\n" %\
                nx.maximum_flow_value(graph, source, sink)
            network_index += 1
