//|enum Color {RED, BLACK, DOUBLE_BLACK}
fn mock() {}
//|class Node {
//|    int data;
//|    int color;
//|    Node *left, *right, *parent;
//|};
//|    
fn mock() {}
//|class RBTree {
//|    Node *root;
//|};
//|    
fn mock() {}
//+[Depends] Node.Node.(int) -> Node
//+class Node {
//+    int data;
//+    int color;
//+    Node *left, *right, *parent;
//+};
//+    
//+-------------------------------------------
//|Node::Node(int data) {
//|    this->data = data;
//|    color = RED;
//|    left = right = parent = nullptr;
//|}
fn mock() {}
//+[Depends] RBTree.RBTree.() -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|RBTree::RBTree() {
//|    root = nullptr;
//|}
fn mock() {}
//+[Depends] RBTree.getColor.(Node*&) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|int RBTree::getColor(Node *&node) {
//|    if (node == nullptr)
//|        return BLACK;
//|
//|    return node->color;
//|}
fn mock() {}
//+[Depends] RBTree.setColor.(Node*&, int) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::setColor(Node *&node, int color) {
//|    if (node == nullptr)
//|        return;
//|
//|    node->color = color;
//|}
fn mock() {}
//+[Depends] RBTree.insertBST.(Node*&, Node*&) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|Node* RBTree::insertBST(Node *&root, Node *&ptr) {
//|    if (root == nullptr)
//|        return ptr;
//|
//|    if (ptr->data < root->data) {
//|        root->left = insertBST(root->left, ptr);
//|        root->left->parent = root;
//|    } else if (ptr->data > root->data) {
//|        root->right = insertBST(root->right, ptr);
//|        root->right->parent = root;
//|    }
//|
//|    return root;
//|}
fn mock() {}
//+[Depends] RBTree.insertValue.(it) -> Node.Node.(int)
//+Node::Node(int data) {
//+    this->data = data;
//+    color = RED;
//+    left = right = parent = nullptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.insertValue.(it) -> RBTree.insertBST.(Node*&, Node*&)
//+Node* RBTree::insertBST(Node *&root, Node *&ptr) {
//+    if (root == nullptr)
//+        return ptr;
//+
//+    if (ptr->data < root->data) {
//+        root->left = insertBST(root->left, ptr);
//+        root->left->parent = root;
//+    } else if (ptr->data > root->data) {
//+        root->right = insertBST(root->right, ptr);
//+        root->right->parent = root;
//+    }
//+
//+    return root;
//+}
//+-------------------------------------------
//+[Depends] RBTree.insertValue.(it) -> RBTree.fixInsertRBTree.(Node*&)
//+void RBTree::fixInsertRBTree(Node *&ptr) {
//+    Node *parent = nullptr;
//+    Node *grandparent = nullptr;
//+    while (ptr != root && getColor(ptr) == RED && getColor(ptr->parent) == RED) {
//+        parent = ptr->parent;
//+        grandparent = parent->parent;
//+        if (parent == grandparent->left) {
//+            Node *uncle = grandparent->right;
//+            if (getColor(uncle) == RED) {
//+                setColor(uncle, BLACK);
//+                setColor(parent, BLACK);
//+                setColor(grandparent, RED);
//+                ptr = grandparent;
//+            } else {
//+                if (ptr == parent->right) {
//+                    rotateLeft(parent);
//+                    ptr = parent;
//+                    parent = ptr->parent;
//+                }
//+                rotateRight(grandparent);
//+                swap(parent->color, grandparent->color);
//+                ptr = parent;
//+            }
//+        } else {
//+            Node *uncle = grandparent->left;
//+            if (getColor(uncle) == RED) {
//+                setColor(uncle, BLACK);
//+                setColor(parent, BLACK);
//+                setColor(grandparent, RED);
//+                ptr = grandparent;
//+            } else {
//+                if (ptr == parent->left) {
//+                    rotateRight(parent);
//+                    ptr = parent;
//+                    parent = ptr->parent;
//+                }
//+                rotateLeft(grandparent);
//+                swap(parent->color, grandparent->color);
//+                ptr = parent;
//+            }
//+        }
//+    }
//+    setColor(root, BLACK);
//+}
//+-------------------------------------------
//+[Depends] RBTree.insertValue.(it) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::insertValue(int n) {
//|    Node *node = new Node(n);
//|    root = insertBST(root, node);
//|    fixInsertRBTree(node);
//|}
fn mock() {}
//+[Depends] RBTree.rotateLeft.(Node*&) -> Node.Node.(int)
//+Node::Node(int data) {
//+    this->data = data;
//+    color = RED;
//+    left = right = parent = nullptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.rotateLeft.(Node*&) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::rotateLeft(Node *&ptr) {
//|    Node *right_child = ptr->right;
//|    ptr->right = right_child->left;
//|
//|    if (ptr->right != nullptr)
//|        ptr->right->parent = ptr;
//|
//|    right_child->parent = ptr->parent;
//|
//|    if (ptr->parent == nullptr)
//|        root = right_child;
//|    else if (ptr == ptr->parent->left)
//|        ptr->parent->left = right_child;
//|    else
//|        ptr->parent->right = right_child;
//|
//|    right_child->left = ptr;
//|    ptr->parent = right_child;
//|}
fn mock() {}
//+[Depends] RBTree.rotateRight.(Node*&) -> Node.Node.(int)
//+Node::Node(int data) {
//+    this->data = data;
//+    color = RED;
//+    left = right = parent = nullptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.rotateRight.(Node*&) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::rotateRight(Node *&ptr) {
//|    Node *left_child = ptr->left;
//|    ptr->left = left_child->right;
//|
//|    if (ptr->left != nullptr)
//|        ptr->left->parent = ptr;
//|
//|    left_child->parent = ptr->parent;
//|
//|    if (ptr->parent == nullptr)
//|        root = left_child;
//|    else if (ptr == ptr->parent->left)
//|        ptr->parent->left = left_child;
//|    else
//|        ptr->parent->right = left_child;
//|
//|    left_child->right = ptr;
//|    ptr->parent = left_child;
//|}
fn mock() {}
//+[Depends] RBTree.fixInsertRBTree.(Node*&) -> Node.Node.(int)
//+Node::Node(int data) {
//+    this->data = data;
//+    color = RED;
//+    left = right = parent = nullptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.fixInsertRBTree.(Node*&) -> RBTree.getColor.(Node*&)
//+int RBTree::getColor(Node *&node) {
//+    if (node == nullptr)
//+        return BLACK;
//+
//+    return node->color;
//+}
//+-------------------------------------------
//+[Depends] RBTree.fixInsertRBTree.(Node*&) -> RBTree.setColor.(Node*&, int)
//+void RBTree::setColor(Node *&node, int color) {
//+    if (node == nullptr)
//+        return;
//+
//+    node->color = color;
//+}
//+-------------------------------------------
//+[Depends] RBTree.fixInsertRBTree.(Node*&) -> RBTree.rotateLeft.(Node*&)
//+void RBTree::rotateLeft(Node *&ptr) {
//+    Node *right_child = ptr->right;
//+    ptr->right = right_child->left;
//+
//+    if (ptr->right != nullptr)
//+        ptr->right->parent = ptr;
//+
//+    right_child->parent = ptr->parent;
//+
//+    if (ptr->parent == nullptr)
//+        root = right_child;
//+    else if (ptr == ptr->parent->left)
//+        ptr->parent->left = right_child;
//+    else
//+        ptr->parent->right = right_child;
//+
//+    right_child->left = ptr;
//+    ptr->parent = right_child;
//+}
//+-------------------------------------------
//+[Depends] RBTree.fixInsertRBTree.(Node*&) -> RBTree.rotateRight.(Node*&)
//+void RBTree::rotateRight(Node *&ptr) {
//+    Node *left_child = ptr->left;
//+    ptr->left = left_child->right;
//+
//+    if (ptr->left != nullptr)
//+        ptr->left->parent = ptr;
//+
//+    left_child->parent = ptr->parent;
//+
//+    if (ptr->parent == nullptr)
//+        root = left_child;
//+    else if (ptr == ptr->parent->left)
//+        ptr->parent->left = left_child;
//+    else
//+        ptr->parent->right = left_child;
//+
//+    left_child->right = ptr;
//+    ptr->parent = left_child;
//+}
//+-------------------------------------------
//+[Depends] RBTree.fixInsertRBTree.(Node*&) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::fixInsertRBTree(Node *&ptr) {
//|    Node *parent = nullptr;
//|    Node *grandparent = nullptr;
//|    while (ptr != root && getColor(ptr) == RED && getColor(ptr->parent) == RED) {
//|        parent = ptr->parent;
//|        grandparent = parent->parent;
//|        if (parent == grandparent->left) {
//|            Node *uncle = grandparent->right;
//|            if (getColor(uncle) == RED) {
//|                setColor(uncle, BLACK);
//|                setColor(parent, BLACK);
//|                setColor(grandparent, RED);
//|                ptr = grandparent;
//|            } else {
//|                if (ptr == parent->right) {
//|                    rotateLeft(parent);
//|                    ptr = parent;
//|                    parent = ptr->parent;
//|                }
//|                rotateRight(grandparent);
//|                swap(parent->color, grandparent->color);
//|                ptr = parent;
//|            }
//|        } else {
//|            Node *uncle = grandparent->left;
//|            if (getColor(uncle) == RED) {
//|                setColor(uncle, BLACK);
//|                setColor(parent, BLACK);
//|                setColor(grandparent, RED);
//|                ptr = grandparent;
//|            } else {
//|                if (ptr == parent->left) {
//|                    rotateRight(parent);
//|                    ptr = parent;
//|                    parent = ptr->parent;
//|                }
//|                rotateLeft(grandparent);
//|                swap(parent->color, grandparent->color);
//|                ptr = parent;
//|            }
//|        }
//|    }
//|    setColor(root, BLACK);
//|}
fn mock() {}
//+[Depends] RBTree.fixDeleteRBTree.(Node*&) -> RBTree.getColor.(Node*&)
//+int RBTree::getColor(Node *&node) {
//+    if (node == nullptr)
//+        return BLACK;
//+
//+    return node->color;
//+}
//+-------------------------------------------
//+[Depends] RBTree.fixDeleteRBTree.(Node*&) -> Node.Node.(int)
//+Node::Node(int data) {
//+    this->data = data;
//+    color = RED;
//+    left = right = parent = nullptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.fixDeleteRBTree.(Node*&) -> RBTree.setColor.(Node*&, int)
//+void RBTree::setColor(Node *&node, int color) {
//+    if (node == nullptr)
//+        return;
//+
//+    node->color = color;
//+}
//+-------------------------------------------
//+[Depends] RBTree.fixDeleteRBTree.(Node*&) -> RBTree.rotateLeft.(Node*&)
//+void RBTree::rotateLeft(Node *&ptr) {
//+    Node *right_child = ptr->right;
//+    ptr->right = right_child->left;
//+
//+    if (ptr->right != nullptr)
//+        ptr->right->parent = ptr;
//+
//+    right_child->parent = ptr->parent;
//+
//+    if (ptr->parent == nullptr)
//+        root = right_child;
//+    else if (ptr == ptr->parent->left)
//+        ptr->parent->left = right_child;
//+    else
//+        ptr->parent->right = right_child;
//+
//+    right_child->left = ptr;
//+    ptr->parent = right_child;
//+}
//+-------------------------------------------
//+[Depends] RBTree.fixDeleteRBTree.(Node*&) -> RBTree.rotateRight.(Node*&)
//+void RBTree::rotateRight(Node *&ptr) {
//+    Node *left_child = ptr->left;
//+    ptr->left = left_child->right;
//+
//+    if (ptr->left != nullptr)
//+        ptr->left->parent = ptr;
//+
//+    left_child->parent = ptr->parent;
//+
//+    if (ptr->parent == nullptr)
//+        root = left_child;
//+    else if (ptr == ptr->parent->left)
//+        ptr->parent->left = left_child;
//+    else
//+        ptr->parent->right = left_child;
//+
//+    left_child->right = ptr;
//+    ptr->parent = left_child;
//+}
//+-------------------------------------------
//+[Depends] RBTree.fixDeleteRBTree.(Node*&) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::fixDeleteRBTree(Node *&node) {
//|    if (node == nullptr)
//|        return;
//|
//|    if (node == root) {
//|        root = nullptr;
//|        return;
//|    }
//|
//|    if (getColor(node) == RED || getColor(node->left) == RED || getColor(node->right) == RED) {
//|        Node *child = node->left != nullptr ? node->left : node->right;
//|
//|        if (node == node->parent->left) {
//|            node->parent->left = child;
//|            if (child != nullptr)
//|                child->parent = node->parent;
//|            setColor(child, BLACK);
//|            delete (node);
//|        } else {
//|            node->parent->right = child;
//|            if (child != nullptr)
//|                child->parent = node->parent;
//|            setColor(child, BLACK);
//|            delete (node);
//|        }
//|    } else {
//|        Node *sibling = nullptr;
//|        Node *parent = nullptr;
//|        Node *ptr = node;
//|        setColor(ptr, DOUBLE_BLACK);
//|        while (ptr != root && getColor(ptr) == DOUBLE_BLACK) {
//|            parent = ptr->parent;
//|            if (ptr == parent->left) {
//|                sibling = parent->right;
//|                if (getColor(sibling) == RED) {
//|                    setColor(sibling, BLACK);
//|                    setColor(parent, RED);
//|                    rotateLeft(parent);
//|                } else {
//|                    if (getColor(sibling->left) == BLACK && getColor(sibling->right) == BLACK) {
//|                        setColor(sibling, RED);
//|                        if(getColor(parent) == RED)
//|                            setColor(parent, BLACK);
//|                        else
//|                            setColor(parent, DOUBLE_BLACK);
//|                        ptr = parent;
//|                    } else {
//|                        if (getColor(sibling->right) == BLACK) {
//|                            setColor(sibling->left, BLACK);
//|                            setColor(sibling, RED);
//|                            rotateRight(sibling);
//|                            sibling = parent->right;
//|                        }
//|                        setColor(sibling, parent->color);
//|                        setColor(parent, BLACK);
//|                        setColor(sibling->right, BLACK);
//|                        rotateLeft(parent);
//|                        break;
//|                    }
//|                }
//|            } else {
//|                sibling = parent->left;
//|                if (getColor(sibling) == RED) {
//|                    setColor(sibling, BLACK);
//|                    setColor(parent, RED);
//|                    rotateRight(parent);
//|                } else {
//|                    if (getColor(sibling->left) == BLACK && getColor(sibling->right) == BLACK) {
//|                        setColor(sibling, RED);
//|                        if (getColor(parent) == RED)
//|                            setColor(parent, BLACK);
//|                        else
//|                            setColor(parent, DOUBLE_BLACK);
//|                        ptr = parent;
//|                    } else {
//|                        if (getColor(sibling->left) == BLACK) {
//|                            setColor(sibling->right, BLACK);
//|                            setColor(sibling, RED);
//|                            rotateLeft(sibling);
//|                            sibling = parent->left;
//|                        }
//|                        setColor(sibling, parent->color);
//|                        setColor(parent, BLACK);
//|                        setColor(sibling->left, BLACK);
//|                        rotateRight(parent);
//|                        break;
//|                    }
//|                }
//|            }
//|        }
//|        if (node == node->parent->left)
//|            node->parent->left = nullptr;
//|        else
//|            node->parent->right = nullptr;
//|        delete(node);
//|        setColor(root, BLACK);
//|    }
//|}
fn mock() {}
//+[Depends] RBTree.deleteBST.(Node*&, int) -> Node.Node.(int)
//+Node::Node(int data) {
//+    this->data = data;
//+    color = RED;
//+    left = right = parent = nullptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.deleteBST.(Node*&, int) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|Node* RBTree::deleteBST(Node *&root, int data) {
//|    if (root == nullptr)
//|        return root;
//|
//|    if (data < root->data)
//|        return deleteBST(root->left, data);
//|
//|    if (data > root->data)
//|        return deleteBST(root->right, data);
//|
//|    if (root->left == nullptr || root->right == nullptr)
//|        return root;
//|
//|    Node *temp = minValueNode(root->right);
//|    root->data = temp->data;
//|    return deleteBST(root->right, temp->data);
//|}
fn mock() {}
//+[Depends] RBTree.deleteValue.(int) -> Node.Node.(int)
//+Node::Node(int data) {
//+    this->data = data;
//+    color = RED;
//+    left = right = parent = nullptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.deleteValue.(int) -> RBTree.fixDeleteRBTree.(Node*&)
//+void RBTree::fixDeleteRBTree(Node *&node) {
//+    if (node == nullptr)
//+        return;
//+
//+    if (node == root) {
//+        root = nullptr;
//+        return;
//+    }
//+
//+    if (getColor(node) == RED || getColor(node->left) == RED || getColor(node->right) == RED) {
//+        Node *child = node->left != nullptr ? node->left : node->right;
//+
//+        if (node == node->parent->left) {
//+            node->parent->left = child;
//+            if (child != nullptr)
//+                child->parent = node->parent;
//+            setColor(child, BLACK);
//+            delete (node);
//+        } else {
//+            node->parent->right = child;
//+            if (child != nullptr)
//+                child->parent = node->parent;
//+            setColor(child, BLACK);
//+            delete (node);
//+        }
//+    } else {
//+        Node *sibling = nullptr;
//+        Node *parent = nullptr;
//+        Node *ptr = node;
//+        setColor(ptr, DOUBLE_BLACK);
//+        while (ptr != root && getColor(ptr) == DOUBLE_BLACK) {
//+            parent = ptr->parent;
//+            if (ptr == parent->left) {
//+                sibling = parent->right;
//+                if (getColor(sibling) == RED) {
//+                    setColor(sibling, BLACK);
//+                    setColor(parent, RED);
//+                    rotateLeft(parent);
//+                } else {
//+                    if (getColor(sibling->left) == BLACK && getColor(sibling->right) == BLACK) {
//+                        setColor(sibling, RED);
//+                        if(getColor(parent) == RED)
//+                            setColor(parent, BLACK);
//+                        else
//+                            setColor(parent, DOUBLE_BLACK);
//+                        ptr = parent;
//+                    } else {
//+                        if (getColor(sibling->right) == BLACK) {
//+                            setColor(sibling->left, BLACK);
//+                            setColor(sibling, RED);
//+                            rotateRight(sibling);
//+                            sibling = parent->right;
//+                        }
//+                        setColor(sibling, parent->color);
//+                        setColor(parent, BLACK);
//+                        setColor(sibling->right, BLACK);
//+                        rotateLeft(parent);
//+                        break;
//+                    }
//+                }
//+            } else {
//+                sibling = parent->left;
//+                if (getColor(sibling) == RED) {
//+                    setColor(sibling, BLACK);
//+                    setColor(parent, RED);
//+                    rotateRight(parent);
//+                } else {
//+                    if (getColor(sibling->left) == BLACK && getColor(sibling->right) == BLACK) {
//+                        setColor(sibling, RED);
//+                        if (getColor(parent) == RED)
//+                            setColor(parent, BLACK);
//+                        else
//+                            setColor(parent, DOUBLE_BLACK);
//+                        ptr = parent;
//+                    } else {
//+                        if (getColor(sibling->left) == BLACK) {
//+                            setColor(sibling->right, BLACK);
//+                            setColor(sibling, RED);
//+                            rotateLeft(sibling);
//+                            sibling = parent->left;
//+                        }
//+                        setColor(sibling, parent->color);
//+                        setColor(parent, BLACK);
//+                        setColor(sibling->left, BLACK);
//+                        rotateRight(parent);
//+                        break;
//+                    }
//+                }
//+            }
//+        }
//+        if (node == node->parent->left)
//+            node->parent->left = nullptr;
//+        else
//+            node->parent->right = nullptr;
//+        delete(node);
//+        setColor(root, BLACK);
//+    }
//+}
//+-------------------------------------------
//+[Depends] RBTree.deleteValue.(int) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::deleteValue(int data) {
//|    Node *node = deleteBST(root, data);
//|    fixDeleteRBTree(node);
//|}
fn mock() {}
//+[Depends] RBTree.inorderBST.(Node*&) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::inorderBST(Node *&ptr) {
//|    if (ptr == nullptr)
//|        return;
//|
//|    inorderBST(ptr->left);
//|    cout << ptr->data << " " << ptr->color << endl;
//|    inorderBST(ptr->right);
//|}
fn mock() {}
//+[Depends] RBTree.inorder.() -> RBTree.inorderBST.(Node*&)
//+void RBTree::inorderBST(Node *&ptr) {
//+    if (ptr == nullptr)
//+        return;
//+
//+    inorderBST(ptr->left);
//+    cout << ptr->data << " " << ptr->color << endl;
//+    inorderBST(ptr->right);
//+}
//+-------------------------------------------
//+[Depends] RBTree.inorder.() -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::inorder() {
//|    inorderBST(root);
//|}
fn mock() {}
//+[Depends] RBTree.preorderBST.(Node*&) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::preorderBST(Node *&ptr) {
//|    if (ptr == nullptr)
//|        return;
//|
//|    cout << ptr->data << " " << ptr->color << endl;
//|    preorderBST(ptr->left);
//|    preorderBST(ptr->right);
//|}
fn mock() {}
//+[Depends] RBTree.preorder.() -> RBTree.preorderBST.(Node*&)
//+void RBTree::preorderBST(Node *&ptr) {
//+    if (ptr == nullptr)
//+        return;
//+
//+    cout << ptr->data << " " << ptr->color << endl;
//+    preorderBST(ptr->left);
//+    preorderBST(ptr->right);
//+}
//+-------------------------------------------
//+[Depends] RBTree.preorder.() -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::preorder() {
//|    preorderBST(root);
//|    cout << "-------" << endl;
//|}
fn mock() {}
//+[Depends] RBTree.minValueNode.(Node*&) -> Node.Node.(int)
//+Node::Node(int data) {
//+    this->data = data;
//+    color = RED;
//+    left = right = parent = nullptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.minValueNode.(Node*&) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|Node *RBTree::minValueNode(Node *&node) {
//|
//|    Node *ptr = node;
//|
//|    while (ptr->left != nullptr)
//|        ptr = ptr->left;
//|
//|    return ptr;
//|}
fn mock() {}
//+[Depends] RBTree.maxValueNode.(Node*&) -> Node.Node.(int)
//+Node::Node(int data) {
//+    this->data = data;
//+    color = RED;
//+    left = right = parent = nullptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.maxValueNode.(Node*&) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|Node* RBTree::maxValueNode(Node *&node) {
//|    Node *ptr = node;
//|
//|    while (ptr->right != nullptr)
//|        ptr = ptr->right;
//|
//|    return ptr;
//|}
fn mock() {}
//+[Depends] RBTree.getBlackHeight.(Node*) -> RBTree.getColor.(Node*&)
//+int RBTree::getColor(Node *&node) {
//+    if (node == nullptr)
//+        return BLACK;
//+
//+    return node->color;
//+}
//+-------------------------------------------
//+[Depends] RBTree.getBlackHeight.(Node*) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|int RBTree::getBlackHeight(Node *node) {
//|    int blackheight = 0;
//|    while (node != nullptr) {
//|        if (getColor(node) == BLACK)
//|            blackheight++;
//|        node = node->left;
//|    }
//|    return blackheight;
//|}
fn mock() {}
//+[Depends] RBTree.merge.(RBTree) -> Node.Node.(int)
//+Node::Node(int data) {
//+    this->data = data;
//+    color = RED;
//+    left = right = parent = nullptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.merge.(RBTree) -> RBTree.maxValueNode.(Node*&)
//+Node* RBTree::maxValueNode(Node *&node) {
//+    Node *ptr = node;
//+
//+    while (ptr->right != nullptr)
//+        ptr = ptr->right;
//+
//+    return ptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.merge.(RBTree) -> RBTree.deleteValue.(int)
//+void RBTree::deleteValue(int data) {
//+    Node *node = deleteBST(root, data);
//+    fixDeleteRBTree(node);
//+}
//+-------------------------------------------
//+[Depends] RBTree.merge.(RBTree) -> RBTree.minValueNode.(Node*&)
//+Node *RBTree::minValueNode(Node *&node) {
//+
//+    Node *ptr = node;
//+
//+    while (ptr->left != nullptr)
//+        ptr = ptr->left;
//+
//+    return ptr;
//+}
//+-------------------------------------------
//+[Depends] RBTree.merge.(RBTree) -> RBTree.getBlackHeight.(Node*)
//+int RBTree::getBlackHeight(Node *node) {
//+    int blackheight = 0;
//+    while (node != nullptr) {
//+        if (getColor(node) == BLACK)
//+            blackheight++;
//+        node = node->left;
//+    }
//+    return blackheight;
//+}
//+-------------------------------------------
//+[Depends] RBTree.merge.(RBTree) -> RBTree.setColor.(Node*&, int)
//+void RBTree::setColor(Node *&node, int color) {
//+    if (node == nullptr)
//+        return;
//+
//+    node->color = color;
//+}
//+-------------------------------------------
//+[Depends] RBTree.merge.(RBTree) -> RBTree.getColor.(Node*&)
//+int RBTree::getColor(Node *&node) {
//+    if (node == nullptr)
//+        return BLACK;
//+
//+    return node->color;
//+}
//+-------------------------------------------
//+[Depends] RBTree.merge.(RBTree) -> RBTree.fixInsertRBTree.(Node*&)
//+void RBTree::fixInsertRBTree(Node *&ptr) {
//+    Node *parent = nullptr;
//+    Node *grandparent = nullptr;
//+    while (ptr != root && getColor(ptr) == RED && getColor(ptr->parent) == RED) {
//+        parent = ptr->parent;
//+        grandparent = parent->parent;
//+        if (parent == grandparent->left) {
//+            Node *uncle = grandparent->right;
//+            if (getColor(uncle) == RED) {
//+                setColor(uncle, BLACK);
//+                setColor(parent, BLACK);
//+                setColor(grandparent, RED);
//+                ptr = grandparent;
//+            } else {
//+                if (ptr == parent->right) {
//+                    rotateLeft(parent);
//+                    ptr = parent;
//+                    parent = ptr->parent;
//+                }
//+                rotateRight(grandparent);
//+                swap(parent->color, grandparent->color);
//+                ptr = parent;
//+            }
//+        } else {
//+            Node *uncle = grandparent->left;
//+            if (getColor(uncle) == RED) {
//+                setColor(uncle, BLACK);
//+                setColor(parent, BLACK);
//+                setColor(grandparent, RED);
//+                ptr = grandparent;
//+            } else {
//+                if (ptr == parent->left) {
//+                    rotateRight(parent);
//+                    ptr = parent;
//+                    parent = ptr->parent;
//+                }
//+                rotateLeft(grandparent);
//+                swap(parent->color, grandparent->color);
//+                ptr = parent;
//+            }
//+        }
//+    }
//+    setColor(root, BLACK);
//+}
//+-------------------------------------------
//+[Depends] RBTree.merge.(RBTree) -> RBTree
//+class RBTree {
//+    Node *root;
//+};
//+    
//+-------------------------------------------
//|void RBTree::merge(RBTree rbTree2) {
//|    int temp;
//|    Node *c, *temp_ptr;
//|    Node *root1 = root;
//|    Node *root2 = rbTree2.root;
//|    int initialblackheight1 = getBlackHeight(root1);
//|    int initialblackheight2 = getBlackHeight(root2);
//|    if (initialblackheight1 > initialblackheight2) {
//|        c = maxValueNode(root1);
//|        temp = c->data;
//|        deleteValue(c->data);
//|        root1 = root;
//|    }
//|    else if (initialblackheight2 > initialblackheight1) {
//|        c = minValueNode(root2);
//|        temp = c->data;
//|        rbTree2.deleteValue(c->data);
//|        root2 = rbTree2.root;
//|    }
//|    else {
//|        c = minValueNode(root2);
//|        temp = c->data;
//|        rbTree2.deleteValue(c->data);
//|        root2 = rbTree2.root;
//|        if (initialblackheight1 != getBlackHeight(root2)) {
//|            rbTree2.insertValue(c->data);
//|            root2 = rbTree2.root;
//|            c = maxValueNode(root1);
//|            temp = c->data;
//|            deleteValue(c->data);
//|            root1 = root;
//|        }
//|    }
//|    setColor(c,RED);
//|    int finalblackheight1 = getBlackHeight(root1);
//|    int finalblackheight2 = getBlackHeight(root2);
//|    if (finalblackheight1 == finalblackheight2) {
//|        c->left = root1;
//|        root1->parent = c;
//|        c->right = root2;
//|        root2->parent = c;
//|        setColor(c,BLACK);
//|        c->data = temp;
//|        root = c;
//|    }
//|    else if (finalblackheight2 > finalblackheight1) {
//|        Node *ptr = root2;
//|        while (finalblackheight1 != getBlackHeight(ptr)) {
//|            temp_ptr = ptr;
//|            ptr = ptr->left;
//|        }
//|        Node *ptr_parent;
//|        if (ptr == nullptr)
//|            ptr_parent = temp_ptr;
//|        else
//|            ptr_parent = ptr->parent;
//|        c->left = root1;
//|        if (root1 != nullptr)
//|            root1->parent = c;
//|        c->right = ptr;
//|        if (ptr != nullptr)
//|            ptr->parent = c;
//|        ptr_parent->left = c;
//|        c->parent = ptr_parent;
//|        if (getColor(ptr_parent) == RED) {
//|            fixInsertRBTree(c);
//|        }
//|        else if (getColor(ptr) == RED){
//|            fixInsertRBTree(ptr);
//|        }
//|        c->data = temp;
//|        root = root2;
//|    }
//|    else {
//|        Node *ptr = root1;
//|        while (finalblackheight2 != getBlackHeight(ptr)) {
//|            ptr = ptr->right;
//|        }
//|        Node *ptr_parent = ptr->parent;
//|        c->right = root2;
//|        root2->parent = c;
//|        c->left = ptr;
//|        ptr->parent = c;
//|        ptr_parent->right = c;
//|        c->parent = ptr_parent;
//|        if (getColor(ptr_parent) == RED) {
//|            fixInsertRBTree(c);
//|        }
//|        else if (getColor(ptr) == RED) {
//|            fixInsertRBTree(ptr);
//|        }
//|        c->data = temp;
//|        root = root1;
//|    }
//|    return;
//|}
fn mock() {}
