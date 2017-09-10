#!/usr/bin/env python

'''
    File name: bst.py
    Python Version: 2.7
    Description: Safe, Laser & Mirror code assignment for Ascent.
                 Binary Search Tree.
'''

__author__ = "Matthieu Destephe"
__email__ = "matt@atomutek.org"


class Node:

    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None


def insert(root, node):
    if root is None:
        root = node
    else:
        if root.value > node.value:
            if root.left is None:
                root.left = node
            else:
                insert(root.left, node)
        else:
            if root.right is None:
                root.right = node
            else:
                insert(root.right, node)

def delete(node, val):
    if node.value == val:
        if node.right and node.left:
            [parent, child] = find_min(node.right, node)
            if parent.left == child:
                parent.left = child.right
            else:
                parent.right = child.right

            child.left = node.left
            child.right = node.right

            return child

        else:
            if node.left:
                return node.left
            else:
                return node.right
    else:
        if node.value > val:
            if node.left:
                node.left = delete(node.left, node)
        else:
            if node.right:
                node.right = delete(node.right, val)

        return node

def find_min(node, parent):
    if node.left:
        return findMin(node.left, node)
    else:
        return [parent, node]


def search_range(root, minimum, maximum):
    nodes = []

    def recursive_search(node):
        if node is None:
            return None

        if node.value > minimum:
            recursive_search(node.left)
        if minimum < node.value < maximum:
            nodes.append(node.value)
        if node.value < maximum:
            recursive_search(node.right)

    recursive_search(root)
    return nodes

if __name__ == "__main__":
    r = Node(3)
    insert(r, Node(7))
    insert(r, Node(1))
    insert(r, Node(5))
    insert(r, Node(10))
    insert(r, Node(6))

    print search_range(r, 4,8)

    delete(r,7)

    print search_range(r, 4,8)
