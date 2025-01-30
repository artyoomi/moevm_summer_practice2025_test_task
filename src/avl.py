from typing import List, Optional
import queue

class AVL:
    class Node:
        """Node for AVL tree class implementation"""
        def __init__(self, key: int, left: Optional['AVL.Node'] = None, right: Optional['AVL.Node'] = None):
            self.key = key
            self.left = left
            self.right = right
            self.height = 1

    def __init__(self):
        self._root = None

    def __del__(self):
        self.clear()

    #=========================#
    # CLASS INTERFACE METHODS #
    #=========================#
    def height(self) -> int:
        """Get height of tree"""
        return self._height(self._root)

    def insert(self, key: int) -> None:
        """Insert new element in tree"""
        self._root = self._run_insert(self._root, key)

    def remove(self, key: int) -> None:
        """Remove specified element from tree"""
        self._root = self._run_remove(self._root, key)

    def remove_min(self) -> None:
        """Remove min element from tree"""
        self._root = self._run_remove_min(self._root)

    def remove_max(self) -> None:
        """Remove max element from tree"""
        self._root = self._run_remove_max(self._root)

    def min(self) -> int:
        """Get min element in tree"""
        min_node = self._min(self._root)
        if min_node is None:
            raise ValueError("AVL tree is empty!")
        return min_node.key

    def max(self) -> int:
        """Get max element in tree"""
        max_node = self._max(self._root)
        if max_node is None:
            raise ValueError("AVL tree is empty!")
        return max_node.key

    def get_keys(self, order: str) -> List[int]:
        """Get elements of tree in specified order"""
        keys = []
        if order == "in":
            self._get_in_order(self._root, keys)
        elif order == "pre":
            self._get_pre_order(self._root, keys)
        elif order == "post":
            self._get_post_order(self._root, keys)
        # elif order == "width":
        #     self._get_width_traversal(self._root, keys)
        else:
            raise ValueError("Unknown traversal order!")
        return keys

    def print(self, order: str = "in") -> None:
        """Print tree elements in console"""
        keys = self.get_keys(order)
        print(" ".join(map(str, keys)))

    def generate_DOT_file(self) -> None:
        """Generate .dot format file for visualization"""
        self._generate_DOT_file(self._root)

    def clear(self) -> None:
        """Empty tree"""
        self._run_clear(self._root)

    #=======================#
    # CLASS BACKEND METHODS #
    #=======================#
    def _height(self, node: Optional[Node]) -> int:
        """Backend function to get height of tree"""
        if node is None:
            return 0
        return node.height

    def _recalc_height(self, node: Node) -> None:
        """Function to recalculate height of specified node"""
        node.height = 1 + max(self._height(node.left),
                              self._height(node.right))

    def _calc_bfactor(self, node: Node) -> int:
        """Function to calculate balance factor of current node"""
        return self._height(node.right) - self._height(node.left)

    def _run_left_rotation(self, rotate_root: Node) -> Node:
        """Function to do left rotation in rotate_node"""

        """   
        We have these tree (balance factor in brackets):
        A(-2)               B(-1)
          \                /    \
          B(-1)     ->   A(-1)  C(0) 
          /  \             \
        D(0)  C(0)        D(0)
        
        Logic of rotation:
        1. B - new root 
        2. A - new left of B
        
        If B have children, then this children become new A right subtree
        """
        new_root = rotate_root.right
        old_new_root_left = new_root.left

        new_root.left = rotate_root
        new_root.left.right = old_new_root_left

        self._recalc_height(rotate_root)
        self._recalc_height(new_root)

        return new_root

    def _run_right_rotation(self, rotate_root: Node) -> Node:
        """Do right rotation in rotate_node"""
        
        new_root = rotate_root.left
        old_new_root_right = new_root.right

        new_root.right = rotate_root
        new_root.right.left = old_new_root_right

        self._recalc_height(rotate_root)
        self._recalc_height(new_root)

        return new_root

    def _run_balancing(self, rotate_node: Node) -> Node:
        """Function to do left rotation in rotate_nod"""
        bfactor = self._calc_bfactor(rotate_node)

        if -2 < bfactor < 2:
            return rotate_node

        if bfactor >= 2:
            if self._calc_bfactor(rotate_node.right) >= 0:
                return self._run_left_rotation(rotate_node)
            else:
                rotate_node.right = self._run_right_rotation(rotate_node.right)
                return self._run_left_rotation(rotate_node)
        else:
            if self._calc_bfactor(rotate_node.left) <= 0:
                return self._run_right_rotation(rotate_node)
            else:
                rotate_node.left = self._run_left_rotation(rotate_node.left)
                return self._run_right_rotation(rotate_node)

    def _run_insert(self, node: Optional[Node], key: int) -> Node:
        if node is None:
            return self.Node(key)

        if key < node.key:
            node.left = self._run_insert(node.left, key)
        else:
            node.right = self._run_insert(node.right, key)

        self._recalc_height(node)
        return self._run_balancing(node)

    def _min(self, root: Optional[Node]) -> Optional[Node]:
        if root is None:
            return None

        current = root
        while current.left is not None:
            current = current.left

        return current

    def _max(self, root: Optional[Node]) -> Optional[Node]:
        if root is None:
            return None

        current = root
        while current.right is not None:
            current = current.right

        return current

    def _run_remove(self, node: Optional[Node], key: int) -> Optional[Node]:
        if node is None:
            return None

        if key < node.key:
            node.left = self._run_remove(node.left, key)
        elif key > node.key:
            node.right = self._run_remove(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                tmp_key = self._min(node.right).key
                node.key = tmp_key
                node.right = self._run_remove(node.right, tmp_key)

        self._recalc_height(node)
        return self._run_balancing(node)

    def _run_remove_min(self, node: Optional[Node]) -> Optional[Node]:
        min_node = self._min(node)
        if min_node is not None:
            return self._run_remove(node, min_node.key)
        return node

    def _run_remove_max(self, node: Optional[Node]) -> Optional[Node]:
        max_node = self._max(node)
        if max_node is not None:
            return self._run_remove(node, max_node.key)
        return node

    def _run_clear(self, node: Optional[Node]) -> None:
        if node is None:
            return
        self._run_clear(node.left)
        self._run_clear(node.right)
        node.left = None
        node.right = None

    def _get_in_order(self, node: Optional[Node], keys: List[int]) -> None:
        if node is None:
            return
        self._get_in_order(node.left, keys)
        keys.append(node.key)
        self._get_in_order(node.right, keys)

    def _get_pre_order(self, node: Optional[Node], keys: List[int]) -> None:
        if node is None:
            return
        keys.append(node.key)
        self._get_pre_order(node.left, keys)
        self._get_pre_order(node.right, keys)

    def _get_post_order(self, node: Optional[Node], keys: List[int]) -> None:
        if node is None:
            return
        self._get_post_order(node.left, keys)
        self._get_post_order(node.right, keys)
        keys.append(node.key)

    def _get_wixdth_traversal(self, root: Optional[Node], keys: List[int]) -> None:
        if root is None:
            return

        q = queue.Queue()
        q.put(root)

        while not q.empty():
            current = q.get()
            keys.append(current.key)

            if current.left is not None:
                q.put(current.left)
            if current.right is not None:
                q.put(current.right)

    def _generate_DOT(self, root: Optional[Node], out) -> None:
        if root is None:
            return

        def form_node(node: self.Node):
            out.write(f'"{node.key}\\nbfactor: {self._calc_bfactor(node)}\\nheight: {node.height}"')

        if root.left:
            out.write("    ")
            form_node(root)
            out.write(" -> ")
            form_node(root.left)
            out.write(";\n")
            self._generate_DOT(root.left, out)

        if root.right:
            out.write("    ")
            form_node(root)
            out.write(" -> ")
            form_node(root.right)
            out.write(";\n")
            self._generate_DOT(root.right, out)

    def _generate_DOT_file(self, root: Optional[Node]) -> None:
        with open("avl_tree.dot", "w") as out:
            out.write("digraph AVLTree {\n")
            out.write("    node [fontname=\"Liberation Mono\"];\n")

            if root is None:
                out.write("    null;\n")
            elif root.left is None and root.right is None:
                out.write(f"    {root.key};\n")
            else:
                self._generate_DOT(root, out)

            out.write("}\n")

    #===============#
    # MAGIC METHODS #
    #===============#
    def __len__(self):
        pass

    def __contains__(self):
        pass

if __name__ == "__main__":
    avl = AVL()

    for i in range(1, 100):
        avl.insert(i)

    avl.generate_DOT_file()
