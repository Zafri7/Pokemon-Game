""" AVL Tree implemented on top of the standard BST. """
#comment testing

__author__ = 'Alexey Ignatiev'
__docformat__ = 'reStructuredText'

"""
Authors: 	1) Tuan Muhammad Zafri
 		    2) Wang Qian
 		    3) Mohammed Salman Ulumuddin
		    4) Ally Teh Tze-Rou  
Last modified by: Tuan Muhammad Zafri on 29/05/2022 
"""

from bst import BinarySearchTree
from typing import TypeVar, Generic
from node import AVLTreeNode
from stack_adt import ArrayStack

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """


    def __init__(self) -> None:
        """
        A method to initialises an empty Binary Search Tree
        
        Timecomplexity: O(1)
        """

        BinarySearchTree.__init__(self)



    def get_height(self, current: AVLTreeNode) -> int:

        """
        A method to get the height of a node. Return current.height if current is not None. Otherwise, return 0.
        
        Time complexity: O(1) because the if condition checks whether current for None is O(1). 
                         Returning the value 0 or returning the current.height is also O(1)
        """

        if current is not None:
            return current.height
        return 0



    def get_balance(self, current: AVLTreeNode) -> int:

        """
        A method to compute the balance factor for the current sub-tree as the value (right.height - left.height). 
        If current is None, return 0.

        Time complexity: O(1) because the if condition checks whether current for None is O(1). 
                         Returning the value 0 or returning self.get_height(current.right) - self.get_height(current.left) is also O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)



    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:

        """
        A method that attempts to insert an item into the tree, it uses the Key to insert
        it. After insertion, performs sub-tree rotation whenever it becomes
        unbalanced.
        returns the new root of the subtree.

        Time complexity: O(log n) because in an avl tree, it is guarenteed to be balanced and the depth of a tree is always log n where
                         n is the number of nodes in a tree

        """
        if current is None:  # base case: at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        
        # Update height
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))

        # Rebalance if needed
        current = self.rebalance(current)

        return current



    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:

        """
        A method that attempts to delete an item from the tree, it uses the Key to
        determine the node to delete. After deletion,
        performs sub-tree rotation whenever it becomes unbalanced.
        returns the new root of the subtree.

        Time complexity: O(log n) because in an avl tree, it is guarenteed to be balanced and the depth of a tree is always log n where
                         n is the number of nodes in a tree
        """ 
        if current is None:
            raise ValueError("Item not found")
        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else: # if key is found
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left
            
            # Get successor and swap
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        # Update height
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))

        # Rebalance if needed
        current = self.rebalance(current)

        return current



    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        
        """
        A method to perform left rotation of the sub-tree.
        Right child of the current node, i.e. of the root of the target
        sub-tree, should become the new root of the sub-tree.
        Example:

                current                                       child
            /       \                                      /   \
        l-tree     child           -------->        current     r-tree
                    /     \                           /     \
                center     r-tree                 l-tree     center

        Time complexity: O(1)
        """
        r_child = current.right
        r_subchild = r_child.left
        r_child.left = current
        current.right = r_subchild

        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        r_child.height = 1 + max(self.get_height(r_child.left), self.get_height(r_child.right))

        return r_child




    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:

        """
        A method to perform right rotation of the sub-tree.
        Left child of the current node, i.e. of the root of the target
        sub-tree, should become the new root of the sub-tree.
        Example:

                    current                                child
                    /       \                              /     \
                child       r-tree     --------->     l-tree     current
                /     \                                           /     \
        l-tree     center                                 center     r-tree

        Time complexity: O(1)
        """
        l_child = current.left
        l_subchild = l_child.right
        l_child.right = current
        current.left = l_subchild

        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        l_child.height = 1 + max(self.get_height(l_child.left), self.get_height(l_child.right))

        return l_child



    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:

        """
        A method to compute the balance of the current node.
        Do rebalancing of the sub-tree of this node if necessary.
        Rebalancing should be done either by:
        - one left rotate
        - one right rotate
        - a combination of left + right rotate
        - a combination of right + left rotate
        returns the new root of the subtree.

        Time complexity: O(1) since the if condition is only checking get_balance if the current node >= 2 or <= -2.
                         Besides that, calling the function and returning the value is also O(1)
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current



    def kth_largest(self, k: int) -> AVLTreeNode:

        """
        A method that returns the kth largest node in the tree, using recursion. 
        Here k = 1 should give the largest node in the subtree

        Time complexity: O(aux_kthLargegst method), which will be O(log n), where n is the total number of nodes, please refer below
        """
        
        return self.aux_kthLargest(self.root, k)
           


    def aux_kthLargest(self, root, k):

        """
        A helper method that finds the kth largest node in the tree, using recursion. 
        Here k = 1 should give the largest node in the subtree

        Time complexity: O(log n), where n is the total number of nodes.
        This is because this method will only go down the tree log n times.
        When going down a tree to search, I used stack ADT because the push and pop methods are O(1).
        For example, 
        8
        ╟─4
        ║ ╟─2
        ║ ║ ╟─1
        ║ ║ ╙─3
        ║ ╙─6
        ║   ╟─5
        ║   ╙─7
        ╙─12
          ╟─10
          ║ ╟─9
          ║ ╙─11
          ╙─14
            ╟─13
            ╙─15
              ╟─
              ╙─16
        Because we are findin the kth largest so this method will go down right every time. 
        The first time it goes down the path(8,12,10,9,11,14,13,14,16)
        The second time it goes down the path(4,6,5,7)
        The third time it goes down the path(2,3)
        The fourth time it goes down the path(1)
        Note that the path is not in the order as mentioned above, this algorithm will push and pop the nodes that is in that path and 
        the poped node will be from largest to smallest so it returns kth largest. The time complexity of pushing and popping is O(1),
        so for every path, when popping the node, it is O(1). So the time complexity depends on how many times it goes down the tree
        and it will be the depth of the leftmost path(8,4,2,1). AVL is always balance so the it is also the depth of the whole tree.
        Thats why O(log n)
        """
        arr = ArrayStack(self.length)
        
        while True:
            while root:
                arr.push(root)
                root = root.right
            root = arr.pop()
            k -= 1
            if not k:
                return root
            root = root.left
                

    


