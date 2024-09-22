import unittest

from llmcc.parser import parse_doc
from llmcc.compiler import compile_graph
from llmcc.printer import write_graph, print_graph
from llmcc.slicer import *
from llmcc.analyzer import analyze_graph


class TestSlicer(unittest.TestCase):

    @parse_doc()
    def test_query(self, g):
        """
//
// Copied from here: https://github.com/anandarao/Red-Black-Tree
//

#ifndef RED_BLACK_TREE_RBTREE_H
#define RED_BLACK_TREE_RBTREE_H

enum Color {RED, BLACK, DOUBLE_BLACK};

struct Node
{
    int data;
    int color;
    Node *left, *right, *parent;

    explicit Node(int);
};

class RBTree
{
    private:
        Node *root;
    protected:
        void rotateLeft(Node *&);
        void rotateRight(Node *&);
        void fixInsertRBTree(Node *&);
        void fixDeleteRBTree(Node *&);
        void inorderBST(Node *&);
        void preorderBST(Node *&);
        int getColor(Node *&);
        void setColor(Node *&, int);
        Node *minValueNode(Node *&);
        Node *maxValueNode(Node *&);
        Node* insertBST(Node *&, Node *&);
        Node* deleteBST(Node *&, int);
        int getBlackHeight(Node *);
    public:
        RBTree();
        void insertValue(int);
        void deleteValue(int);
        void merge(RBTree);
        void inorder();
        void preorder();
};


#endif //RED_BLACK_TREE_RBTREE_H//
// Red Black Tree Implementation
//
#include <bits/stdc++.h>
#include "rb.h"
using namespace std;

Node::Node(int data) {
    this->data = data;
    color = RED;
    left = right = parent = nullptr;
}

RBTree::RBTree() {
    root = nullptr;
}

int RBTree::getColor(Node *&node) {
    if (node == nullptr)
        return BLACK;

    return node->color;
}
        """
        print_graph(g)
        slice_graph(g)
        analyze_graph(g)
        for k, v in g.node_map.items():
            print(k, v)
        # slice_graph(g)


if __name__ == "__main__":
    unittest.main()
