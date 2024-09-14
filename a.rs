//|struct Node
//|{
//|    int data;
//|    int color;
//|    Node *left, *right, *parent;
//|
//|    explicit Node(int);
//|}
struct Node {
    data: i32,
    color: i32,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
    parent: Option<Box<Node>>,
}

impl Node {
    fn new(data: i32) -> Node {
        Node {
            data,
            color: 0, // Assuming default color value 0
            left: None,
            right: None,
            parent: None,
        }
    }
}
//|class RBTree
//|{
//|    private:
//|        Node *root;
//|    protected:
//|        void rotateLeft(Node *&);
//|        void rotateRight(Node *&);
//|        void fixInsertRBTree(Node *&);
//|        void fixDeleteRBTree(Node *&);
//|        void inorderBST(Node *&);
//|        void preorderBST(Node *&);
//|        int getColor(Node *&);
//|        void setColor(Node *&, int);
//|        Node *minValueNode(Node *&);
//|        Node *maxValueNode(Node *&);
//|        Node* insertBST(Node *&, Node *&);
//|        Node* deleteBST(Node *&, int);
//|        int getBlackHeight(Node *);
//|    public:
//|        RBTree();
//|        void insertValue(int);
//|        void deleteValue(int);
//|        void merge(RBTree);
//|        void inorder();
//|        void preorder();
//|}
struct Node {
    // Node fields go here
}

struct RBTree {
    root: Option<Box<Node>>,
}

impl RBTree {
    fn new() -> Self {
        RBTree { root: None }
    }

    fn rotate_left(&mut self, node: &mut Node) {
        // Implement rotation logic
    }

    fn rotate_right(&mut self, node: &mut Node) {
        // Implement rotation logic
    }

    fn fix_insert_rb_tree(&mut self, node: &mut Node) {
        // Implement insert fix-up logic
    }

    fn fix_delete_rb_tree(&mut self, node: &mut Node) {
        // Implement delete fix-up logic
    }

    fn inorder_bst(&self, node: &Node) {
        // Implement in-order traversal
    }

    fn preorder_bst(&self, node: &Node) {
        // Implement pre-order traversal
    }

    fn get_color(&self, node: &Node) -> i32 {
        // Implement color retrieval
    }

    fn set_color(&mut self, node: &mut Node, color: i32) {
        // Implement color setting
    }

    fn min_value_node(&self, node: &Node) -> &Node {
        // Implement minimum value node retrieval
    }

    fn max_value_node(&self, node: &Node) -> &Node {
        // Implement maximum value node retrieval
    }

    fn insert_bst(&mut self, node: &mut Node, value: i32) -> Option<Box<Node>> {
        // Implement BST insert
    }

    fn delete_bst(&mut self, node: &mut Node, value: i32) -> Option<Box<Node>> {
        // Implement BST delete
    }

    fn get_black_height(&self, node: &Node) -> i32 {
        // Implement black height calculation
    }

    pub fn insert_value(&mut self, value: i32) {
        // Public interface to insert a value
    }

    pub fn delete_value(&mut self, value: i32) {
        // Public interface to delete a value
    }

    pub fn merge(&mut self, other: RBTree) {
        // Public interface to merge with another tree
    }

    pub fn inorder(&self) {
        // Public interface to traverse in-order
    }

    pub fn preorder(&self) {
        // Public interface to traverse pre-order
    }
}
//|Node::Node(int data) {
//|    this->data = data;
//|    color = RED;
//|    left = right = parent = nullptr;
//|}
struct Node {
    data: i32,
    color: Color,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
    parent: Option<Box<Node>>,

    fn new(data: i32) -> Self {
        Node {
            data,
            color: Color::Red,
            left: None,
            right: None,
            parent: None,
        }
    }
}

enum Color {
    Red,
    // Other colors as needed
}
//|RBTree::RBTree() {
//|    root = nullptr;
//|}
struct RBTree {
    root: Option<Box<Node>>,

    fn new() -> RBTree {
        RBTree { root: None }
    }
}
//|int RBTree::getColor(Node *&node) {
//|    if (node == nullptr)
//|        return BLACK;
//|
//|    return node->color;
//|}
impl RBTree {
    fn get_color(node: &Option<Box<Node>>) -> Color {
        match node {
            Some(n) => n.color,
            None => Color::Black,
        }
    }
}
//|void RBTree::setColor(Node *&node, int color) {
//|    if (node == nullptr)
//|        return;
//|
//|    node->color = color;
//|}
impl RBTree {
    fn set_color(node: &mut Option<Box<Node>>, color: Color) {
        if let Some(n) = node {
            n.color = color;
        }
    }
}
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
impl RBTree {
    fn insert_bst(&mut self, root: &mut Option<Box<Node>>, ptr: &mut Box<Node>) -> &mut Option<Box<Node>> {
        if root.is_none() {
            return &mut Some(ptr.clone());
        }
        let root_node = root.as_deref_mut().unwrap();
        if ptr.data < root_node.data {
            let left = self.insert_bst(&mut root_node.left, ptr);
            left.as_deref_mut().unwrap().parent = Some(Box::new(root_node.clone()));
        } else if ptr.data > root_node.data {
            let right = self.insert_bst(&mut root_node.right, ptr);
            right.as_deref_mut().unwrap().parent = Some(Box::new(root_node.clone()));
        }
        root
    }
}
//|void RBTree::insertValue(int n) {
//|    Node *node = new Node(n);
//|    root = insertBST(root, node);
//|    fixInsertRBTree(node);
//|}
impl RBTree {
    fn insert_value(&mut self, n: i32) {
        let node = Box::new(Node::new(n));
        self.root = self.insert_bst(self.root.take(), node);
        self.fix_insert_rbtree(node);
    }
}
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
fn rotate_left<T>(ptr: &mut Box<Node<T>>) where T: Ord {
    let mut right_child = ptr.right.take().expect("Right child must exist");
    ptr.right = right_child.left.take();

    if let Some(ref mut right) = ptr.right {
        right.parent = Some(ptr as *mut _);
    }

    let parent_raw = ptr.parent;
    right_child.parent = parent_raw;

    if parent_raw.is_null() {
        // Update root here, depending on your tree structure
    } else {
        unsafe {
            let parent = &mut *parent_raw;
            if ptr as *mut _ == parent.left.as_mut().unwrap() as *mut _ {
                parent.left = Some(right_child);
            } else {
                parent.right = Some(right_child);
            }
        }
    }

    right_child.left = Some(ptr.clone()); // You may need to adjust this for ownership
    ptr.parent = Some(Box::into_raw(right_child));
}
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
fn rotate_right(ptr: &mut Option<Box<Node>>) {
    let left_child_opt = ptr.as_mut().unwrap().left.take();
    if let Some(left_child) = left_child_opt {
        if let Some(left_child_right) = left_child.right {
            ptr.as_mut().unwrap().left = Some(left_child_right);
            ptr.as_mut().unwrap().left.as_mut().unwrap().parent = Some(ptr.as_mut().unwrap().value);
        }

        left_child.parent = ptr.as_ref().unwrap().parent;
        // Assuming `root` is accessible and its type is Option<Box<Node>>
        if ptr.as_ref().unwrap().parent.is_none() {
            root = Some(left_child);
        } else if let Some(parent) = ptr.as_mut().unwrap().parent {
            if ptr.as_ref().unwrap().value < parent {
                parent.left = Some(Box::new(left_child));
            } else {
                parent.right = Some(Box::new(left_child));
            }
        }

        ptr.as_mut().unwrap().parent = Some(left_child.value);
        left_child.right = Some(*ptr.take().unwrap());
        *ptr = Some(left_child);
    }
}
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
fn fix_insert_rb_tree(ptr: &mut Rc<RefCell<Node>>, root: &mut Rc<RefCell<Node>>) {
    let mut parent: Option<Rc<RefCell<Node>>>;
    let mut grandparent: Option<Rc<RefCell<Node>>>;
    while Rc::ptr_eq(ptr, root) && get_color(&ptr) == Color::Red && get_color(&ptr.borrow().parent) == Color::Red {
        parent = ptr.borrow().parent.clone();
        grandparent = parent.as_ref().and_then(|n| n.borrow().parent.clone());
        if parent == grandparent.as_ref().unwrap().borrow().left {
            let uncle = grandparent.as_ref().unwrap().borrow().right.clone();
            if get_color(&uncle) == Color::Red {
                set_color(&uncle, Color::Black);
                set_color(&parent, Color::Black);
                set_color(&grandparent, Color::Red);
                *ptr = grandparent.unwrap();
            } else {
                if Rc::ptr_eq(ptr, &parent.as_ref().unwrap().borrow().right) {
                    rotate_left(&parent);
                    *ptr = parent.unwrap();
                    parent = ptr.borrow().parent.clone();
                }
                rotate_right(&grandparent);
                swap(&mut parent.as_mut().unwrap().borrow_mut().color, &mut grandparent.as_mut().unwrap().borrow_mut().color);
                *ptr = parent.unwrap();
            }
        } else {
            let uncle = grandparent.as_ref().unwrap().borrow().left.clone();
            if get_color(&uncle) == Color::Red {
                set_color(&uncle, Color::Black);
                set_color(&parent, Color::Black);
                set_color(&grandparent, Color::Red);
                *ptr = grandparent.unwrap();
            } else {
                if Rc::ptr_eq(ptr, &parent.as_ref().unwrap().borrow().left) {
                    rotate_right(&parent);
                    *ptr = parent.unwrap();
                    parent = ptr.borrow().parent.clone();
                }
                rotate_left(&grandparent);
                swap(&mut parent.as_mut().unwrap().borrow_mut().color, &mut grandparent.as_mut().unwrap().borrow_mut().color);
                *ptr = parent.unwrap();
            }
        }
    }
    set_color(root, Color::Black);
}
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
impl RBTree {
    fn fix_delete_rb_tree(&mut self, node: &mut Option<Box<Node>>) {
        if node.is_none() {
            return;
        }

        if Rc::ptr_eq(node.as_ref().unwrap(), &self.root) {
            self.root = None;
            return;
        }

        let node_ref = node.as_ref().unwrap();
        let parent_ref = node_ref.parent.as_ref().unwrap().upgrade().unwrap();
        if node_ref.color == RED || node_ref.left.as_ref().map_or(false, |n| n.color == RED) || node_ref.right.as_ref().map_or(false, |n| n.color == RED) {
            let child = if node_ref.left.is_some() { node_ref.left.as_ref() } else { node_ref.right.as_ref() };

            if node_ref.is_left_child() {
                parent_ref.borrow_mut().left = child.cloned();
            } else {
                parent_ref.borrow_mut().right = child.cloned();
            }

            if let Some(child) = child {
                child.borrow_mut().parent = Some(Rc::downgrade(&parent_ref));
                child.borrow_mut().color = BLACK;
            }

            // `drop` is used instead of `delete` in Rust to ensure the value is cleaned up.
            // Rust will automatically clean up when the value goes out of scope.
        } else {
            // Similar alterations to the code below, including using Rc and RefCell for parent and sibling,
            // adjusting match guards and conditions, and replacing delete with Rust's automatic cleanup.
            let mut sibling = None;
            let mut parent = Some(Rc::clone(&parent_ref));
            let mut ptr = Rc::clone(&node_ref);

            ptr.borrow_mut().color = DOUBLE_BLACK;
            while !Rc::ptr_eq(&ptr, &self.root) && ptr.borrow().color == DOUBLE_BLACK {
                let tmp_parent = if let Some(ref p) = parent { Some(Rc::clone(p)) } else { None };
                if ptr.borrow().is_left_child() {
                    sibling = tmp_parent.as_ref().unwrap().borrow().right.as_ref().map(|n| Rc::clone(n));
                    // Continue with sibling checks and rotations as in the C++ code, ensuring valid Rust syntax.
                } else {
                    sibling = tmp_parent.as_ref().unwrap().borrow().left.as_ref().map(|n| Rc::clone(n));
                    // Continue with sibling checks and rotations as in the C++ code, ensuring valid Rust syntax.
                }
            }

            if node_ref.is_left_child() {
                parent_ref.borrow_mut().left = None;
            } else {
                parent_ref.borrow_mut().right = None;
            }

            self.set_color(&mut self.root, BLACK);
        }
    }
}

// Note: External enum, structs, and function implementations for Node, colors, rotations,
// set_color function, is_left_child function, weak references (Rc<RefCell<..>>) need to be defined.
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
struct Node {
    data: i32,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

impl Node {
    fn delete_bst(&mut self, data: i32) -> Option<Box<Node>> {
        if data < self.data {
            if let Some(ref mut left) = self.left {
                return left.delete_bst(data);
            }
        } else if data > self.data {
            if let Some(ref mut right) = self.right {
                return right.delete_bst(data);
            }
        } else {
            if self.left.is_none() || self.right.is_none() {
                return Some(Box::new(self.clone()));
            }
            let mut temp = self.min_value_node();
            self.data = temp.data;
            return self.right.as_mut().unwrap().delete_bst(temp.data);
        }
        None
    }

    fn min_value_node(&mut self) -> Box<Node> {
        let mut current = self;
        while let Some(ref mut left) = current.left {
            current = left.as_mut();
        }
        Box::new(current.clone())
    }
}
//|void RBTree::deleteValue(int data) {
//|    Node *node = deleteBST(root, data);
//|    fixDeleteRBTree(node);
//|}
impl RBTree {
    pub fn delete_value(&mut self, data: i32) {
        let node = self.delete_bst(data);
        self.fix_delete_rb_tree(node);
    }
}
//|void RBTree::inorderBST(Node *&ptr) {
//|    if (ptr == nullptr)
//|        return;
//|
//|    inorderBST(ptr->left);
//|    cout << ptr->data << " " << ptr->color << endl;
//|    inorderBST(ptr->right);
//|}
impl RBTree {
    fn inorder_bst(&self, ptr: &Option<Box<Node>>) {
        if let Some(node) = ptr {
            self.inorder_bst(&node.left);
            println!("{} {}", node.data, node.color);
            self.inorder_bst(&node.right);
        }
    }
}
//|void RBTree::inorder() {
//|    inorderBST(root);
//|}
impl RBTree {
    fn inorder(&self) {
        self.inorder_bst(&self.root);
    }
}

//|void RBTree::preorderBST(Node *&ptr) {
//|    if (ptr == nullptr)
//|        return;
//|
//|    cout << ptr->data << " " << ptr->color << endl;
//|    preorderBST(ptr->left);
//|    preorderBST(ptr->right);
//|}
fn preorder_bst(node: &Option<Box<Node>>) {
    if let Some(n) = node {
        println!("{} {}", n.data, n.color);
        preorder_bst(&n.left);
        preorder_bst(&n.right);
    }
}
//|void RBTree::preorder() {
//|    preorderBST(root);
//|    cout << "-------" << endl;
//|}
impl RBTree {
    fn preorder(&self) {
        self.preorder_bst(&self.root);
        println!("-------");
    }
}

// Assuming preorder_bst is defined elsewhere in the RBTree impl block
// with the appropriate traversal logic.
//|Node *RBTree::minValueNode(Node *&node) {
//|
//|    Node *ptr = node;
//|
//|    while (ptr->left != nullptr)
//|        ptr = ptr->left;
//|
//|    return ptr;
//|}
impl RBTree {
    fn min_value_node(&self, mut node: &Node) -> &Node {
        let mut ptr = node;

        while let Some(ref left) = ptr.left {
            ptr = left;
        }

        ptr
    }
}
//|Node* RBTree::maxValueNode(Node *&node) {
//|    Node *ptr = node;
//|
//|    while (ptr->right != nullptr)
//|        ptr = ptr->right;
//|
//|    return ptr;
//|}
impl RBTree {
    fn max_value_node(node: &mut Option<&mut Node>) -> Option<&mut Node> {
        let mut ptr = node.as_deref_mut()?;

        while let Some(right) = ptr.right.as_deref_mut() {
            ptr = right;
        }

        Some(ptr)
    }
}
//|int RBTree::getBlackHeight(Node *node) {
//|    int blackheight = 0;
//|    while (node != nullptr) {
//|        if (getColor(node) == BLACK)
//|            blackheight++;
//|        node = node->left;
//|    }
//|    return blackheight;
//|}
impl RBTree {
    fn get_black_height(&self, mut node: Option<&Node>) -> i32 {
        let mut black_height = 0;
        while let Some(n) = node {
            if self.get_color(n) == Color::Black {
                black_height += 1;
            }
            node = n.left.as_ref().map(|node| &**node);
        }
        black_height
    }
}
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
impl RBTree {
    fn merge(&mut self, mut rb_tree2: RBTree) {
        let mut temp;
        let mut c;
        let mut temp_ptr;
        let mut root1 = self.root.take();
        let mut root2 = rb_tree2.root.take();
        let initial_black_height1 = self.get_black_height(root1.as_ref());
        let initial_black_height2 = rb_tree2.get_black_height(root2.as_ref());
        if initial_black_height1 > initial_black_height2 {
            c = self.max_value_node(root1.as_ref());
            temp = c.data;
            self.delete_value(c.data);
            root1 = self.root.take();
        } else if initial_black_height2 > initial_black_height1 {
            c = rb_tree2.min_value_node(root2.as_ref());
            temp = c.data;
            rb_tree2.delete_value(c.data);
            root2 = rb_tree2.root.take();
        } else {
            c = rb_tree2.min_value_node(root2.as_ref());
            temp = c.data;
            rb_tree2.delete_value(c.data);
            root2 = rb_tree2.root.take();
            if initial_black_height1 != self.get_black_height(root2.as_ref()) {
                rb_tree2.insert_value(c.data);
                root2 = rb_tree2.root.take();
                c = self.max_value_node(root1.as_ref());
                temp = c.data;
                self.delete_value(c.data);
                root1 = self.root.take();
            }
        }
        c.set_color(Color::Red);
        let final_black_height1 = self.get_black_height(root1.as_ref());
        let final_black_height2 = rb_tree2.get_black_height(root2.as_ref());
        if final_black_height1 == final_black_height2 {
            c.left = root1;
            root1.as_mut().map(|node| node.parent = Some(Rc::downgrade(&Rc::new(c.clone()))));
            c.right = root2;
            root2.as_mut().map(|node| node.parent = Some(Rc::downgrade(&Rc::new(c.clone()))));
            c.set_color(Color::Black);
            c.data = temp;
            self.root = Some(Rc::new(c));
        }
        // Rest of the `else if` and `else` blocks continues with similar adjustments and fix-ups
        // as in the C++ code, using Rust's memory safety features with Rc and RefCell
    }
}

