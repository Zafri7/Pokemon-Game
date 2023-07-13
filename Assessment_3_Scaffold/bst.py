""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev and Jackson Goerner'
__docformat__ = 'reStructuredText'

"""
Authors: 	1) Tuan Muhammad Zafri
 		    2) Wang Qian
 		    3) Mohammed Salman Ulumuddin
		    4) Ally Teh Tze-Rou  
Last modified by: Ally Teh Tze-Rou on 29/05/2022 
"""

from typing import TypeVar, Generic
from linked_stack import LinkedStack
from node import TreeNode
import sys


# generic types
K = TypeVar('K')
I = TypeVar('I')
T = TypeVar('T')


class BSTInOrderIterator:
    """ In-order iterator for the binary search tree.
        Performs stack-based BST traversal.
    """

    def __init__(self, root: TreeNode[K, I]) -> None:
        """
        A method to initialise the Iterator.
        
        Time complexity: O(1)
        """

        self.stack = LinkedStack()
        self.current = root

    def __iter__(self) -> BSTInOrderIterator:
        """
        Standard __iter__() method for initialisers. Returns itself. 
        
        Time complexity: O(1)
        """
        return self

    def __next__(self) -> K:
        """ 
        The main body of the iterator.
        Returns keys of the BST one by one respecting the in-order.
        #not sure
        Time complexity: O(1)
        """

        while self.current:
            self.stack.push(self.current)
            self.current = self.current.left

        if self.stack.is_empty():
            raise StopIteration

        result = self.stack.pop()
        self.current = result.right

        return result.key


class BinarySearchTree(Generic[K, I]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
        Initialises an empty Binary Search Tree

        Time complexity: O(1)
        """

        self.root = None
        self.length = 0



    def is_empty(self) -> bool:
        """
        A method to check to if the bst is empty

        Time complexity: O(1)
        """
        return self.root is None



    def __len__(self) -> int:
        """ 
        A method that returns the number of nodes in the tree.

        Time complexity: O(1) 
        """
        return self.length



    def __contains__(self, key: K) -> bool:
        """
        A method to check if the key is in the BST

        Time complexity: see __getitem__(self, key: K) -> (K, I)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True



    def __iter__(self) -> BSTInOrderIterator:
        """
        A method to create an in-order iterator. 

        Time complexity: O(1)
        """
        return BSTInOrderIterator(self.root)



    def __getitem__(self, key: K) -> I:
        """
        Attempts to get an item in the tree, it uses the Key to attempt to find it
            :complexity best: O(CompK) finds the item in the root of the tree
            :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
            CompK is the complexity of comparing the keys

        Time complexity: O(get_tree_node_by_key method), pls refer below
        """
        return self.get_tree_node_by_key(key).item



    def get_tree_node_by_key(self, key: K) -> TreeNode:
        """
        A method to get the tree node by key

        Time complexity: O(get_tree_node_by_key_aux method), pls refer below
        """
        return self.get_tree_node_by_key_aux(self.root, key)



    def get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
        A method to get the tree node by comparing the keys of the nodes.

        Time complexity: Best case: O(1) when all nodes are in either left of right subtree.
                         Worst case(balanced): when the node we are finding is at the deppest part of tree
                         O(log N) where N is the number of nodes in the tree. When balanced, the depth of the 
                         tree is log N
                         Worst case(unbalanced): O(N) where N is the number of nodes in the tree. When unbalanced, the depth of the
                         tree is N-1
        """
        if current is None:  # base case: empty
            raise KeyError('Key not found: {0}'.format(key))
        elif key == current.key:  # base case: found
            return current
        elif key < current.key:
            return self.get_tree_node_by_key_aux(current.left, key)
        else:  # key > current.key
            return self.get_tree_node_by_key_aux(current.right, key)



    def getitem_aux(self, current: TreeNode, key: K) -> I:
        """
        A method to get the item from a TreeNode and its key

        Time complexity: Best case: O(1) when all nodes are in either left of right subtree.
                         Worst case(balanced): when the node we are finding is at the deppest part of tree
                         O(log N) where N is the number of nodes in the tree. When balanced, the depth of the 
                         tree is log N
                         Worst case(unbalanced): O(N) where N is the number of nodes in the tree. When unbalanced, the depth of the
                         tree is N-1
        """
        if current is None:  # base case: empty
            raise KeyError('Key not found: {0}'.format(key))
        elif key == current.key:  # base case: found
            return current.item
        elif key < current.key:
            return self.getitem_aux(current.left, key)
        else:  # key > current.key
            return self.getitem_aux(current.right, key)



    def __setitem__(self, key: K, item: I) -> None:
        """
        A method to insert a node into the tree using a key

        Time complexity: O(insert_aux) method, pls refer below
        """
        self.root = self.insert_aux(self.root, key, item)



    def insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode:
        """
        A method that attempts to insert an item into the tree, it uses the Key to insert it
        
        Time complexity: Best case: O(1) when all nodes are in either left of right subtree.
                         Worst case(balanced): when the node we are finding is at the deppest part of tree
                         O(log N) where N is the number of nodes in the tree. When balanced, the depth of the 
                         tree is log N
                         Worst case(unbalanced): O(N) where N is the number of nodes in the tree. When unbalanced, the depth of the
                         tree is N-1
        """
        if current is None:  # base case: at the leaf
            current = TreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        return current



    def __delitem__(self, key: K) -> None:
        """
        A method to delete a node from the tree according to the key

        Time complexity: O(delete_aux() method), pls refer below
        """
        self.root = self.delete_aux(self.root, key)



    def delete_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
        A method that attempts to delete an item from the tree, it uses the Key to
        determine the node to delete.

       Time complexity: Best case: O(1) when all nodes are in either left of right subtree.
                        Worst case(balanced): when the node we are finding is at the deppest part of tree
                        O(log N) where N is the number of nodes in the tree. When balanced, the depth of the 
                        tree is log N
                        Worst case(unbalanced): O(N) where N is the number of nodes in the tree. When unbalanced, the depth of the
                        tree is N-1
                        The deletion of nodes is O(1) because get_successor is O(1).

        """
        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        return current



    def get_successor(self, current: TreeNode) -> TreeNode: #Ally did
        """
        Get successor of the current node.
        It should be a child node having the smallest key among all the
        larger keys.

        Time complexity: O(1)
        """
        if current.right is not None:
            return self.get_minimal(current.right)
        else:
            return None



    def get_minimal(self, current: TreeNode) -> TreeNode:
        """
        A method to get a node that has the smallest key in the current sub-tree.
        Clearly, due to the properties of BST, it should be the
        left-most node.

        Time complexity: O(1)
        """
        if current.left is None:
            return current
        else:
            return self.get_minimal(current.left)



    def is_leaf(self, current: TreeNode) -> bool:
        """
        A method that does a simple check whether or not the node is a leaf.

        Time complexity: O(1)
        """

        return current.left is None and current.right is None



    def draw(self, to=sys.stdout):
        """
        A method that draws the tree in the terminal.

        Time complexity: O(1)
        """

        # get the nodes of the graph to draw recursively
        self.draw_aux(self.root, prefix='', final='', to=to)



    def draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout) -> K:
        """
        Draw a node and then its children.
        
        Time complexity: O(1)
        """

        if current is not None:
            real_prefix = prefix[:-2] + final
            print('{0}{1}'.format(real_prefix, str(current.key)), file=to)

            if current.left or current.right:
                self.draw_aux(current.left,  prefix=prefix + '\u2551 ', final='\u255f\u2500', to=to)
                self.draw_aux(current.right, prefix=prefix + '  ', final='\u2559\u2500', to=to)
        else:
            real_prefix = prefix[:-2] + final
            print('{0}'.format(real_prefix), file=to)