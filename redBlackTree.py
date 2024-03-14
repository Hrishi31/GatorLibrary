class Node:
    def __init__(self, key, value=None, color="RED"):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.color = color


class RedBlackTree:
    def __init__(self):
        self.root = None
        self.color_flips = 0  # Initialize the color flip counter

    def is_red(self, node):
        # returns True if the given node is red, False otherwise.
        if not node:
            return False
        return node.color == "RED"

    def rotate_left(self, node):
        # performs a left rotation on the given node and its right child, and returns the new root of the subtree.
        right = node.right
        node.right = right.left
        right.left = node
        right.color = node.color
        node.color = "RED"
        if self.is_red(node.right) and not self.is_red(node.left):
            self.color_flips += 1
        return right

    def rotate_right(self, node):
        # performs a right rotation on the given node and its left child, and returns the new root of the subtree.
        left = node.left
        node.left = left.right
        left.right = node
        left.color = node.color
        node.color = "RED"
        if self.is_red(node.left) and self.is_red(node.left.left):
            self.color_flips += 1
        return left

    def flip_colors(self, node):
        # flips the colors of the given node and its two children.
        node.color = "RED"
        node.left.color = "BLACK"
        node.right.color = "BLACK"
        if self.is_red(node.left) and self.is_red(node.right):
            self.color_flips += 1

    def put(self, key, value=None):
        """
        inserts a new node with the given key and value (if specified) into the tree. 
        If the key already exists in the tree, its value is updated.
        """
        self.root = self._put(self.root, key, value)
        self.root.color = "BLACK"

    def _put(self, node, key, value=None):
        # is a helper function for put() that inserts a new node into the subtree rooted at the given node.
        if not node:
            return Node(key, value)

        if key.book_id < node.key.book_id:
            node.left = self._put(node.left, key, value)
        elif key.book_id > node.key.book_id:
            node.right = self._put(node.right, key, value)
        else:
            node.key.value = value

        if self.is_red(node.right) and not self.is_red(node.left):
            node = self.rotate_left(node)
            self.color_flips += 1
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)
            self.color_flips += 1
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)
            self.color_flips += 1

        return node

    def get(self, key):
        # returns the value associated with the given key in the tree, or None if the key is not found.
        node = self.root
        while node:
            if key == node.key.book_id:
                return node
            elif key < node.key.book_id:
                node = node.left
            else:
                node = node.right

        return None

    def delete(self, key):
        # removes the node with the given key from the tree.
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        # is a helper function for delete() that removes the node with the given key from the subtree rooted at the given node.
        if not node:
            return None
        if key < node.key.book_id:
            node.left = self._delete(node.left, key)
        elif key > node.key.book_id:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                successor = self._get_min(node.right)
                node.key = successor.key
                node.value = successor.value
                node.right = self._delete(node.right, successor.key.book_id)

        if self.is_red(node.right) and not self.is_red(node.left):
            node = self.rotate_left(node)
            self.color_flips += 1
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)
            self.color_flips += 1
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)
            self.color_flips += 1

        return node

    def _get_min(self, node):
        # returns the node with the minimum key in the subtree rooted at the given node.
        while node.left:
            node = node.left
        return node

    def inorder_traversal(self, start_key, end_key):
        """
        Returns a list of nodes in the tree, in order, from start_key to end_key (inclusive).
        """
        nodes = []
        self._inorder_traversal(self.root, start_key, end_key, nodes)
        return nodes

    def _inorder_traversal(self, node, start_key, end_key, nodes):
        if not node:
            return
        if start_key < node.key.book_id:
            self._inorder_traversal(node.left, start_key, end_key, nodes)

        if start_key <= node.key.book_id and end_key >= node.key.book_id:
            nodes.append(node)

        if end_key > node.key.book_id:
            self._inorder_traversal(node.right, start_key, end_key, nodes)

    def get_color_flips(self):
        return self.color_flips