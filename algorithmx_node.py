class AlgorithmXNode:
    def __init__(self, value=0) -> None:
        self.value = value
        self.left = self.right = self.up = self.down = self.top = (
            self  # Each node connecting the all the other nodes
        )

    def insert_h(self) -> None:
        """This is responsible for inserting node to rows of nodes"""
        self.left.right = self.right.left = self

    def insert_v(self, update_top=True):
        """
        This method is responsible for inserting node
        to the column of node
        """
        self.up.down = self.down.up
        if update_top:
            self.top += 1

    def insert_above(self, node) -> None:
        """This method place a new node and then update the top node accordingly

        Args:
            node (node): Node of linked list
        """
        self.top = node.top
        self.up = node.up
        self.down = node

        self.insert_v()

    def insert_after(self, node) -> None:
        """This method place node after a specific node

        Args:
            node (node): This is the node for the Dancing linked list
        """

        self.right = node.right
        self.left = node
        self.insert_h()

    def remove_h(self) -> None:
        """Remove this node from the row. Inverse of insert_h()"""

        self.left.right = self.right
        self.right.left = self.left

    def remove_v(self, update_top=True) -> None:
        """Remove this node from the column inverse of the the inverse_v

        Args:
            update_top (bool, optional): This indicates wether we need to update the top or not. Defaults to True.
        """

        self.up.down = self.down
        self.down.up = self.up
        if update_top:
            self.top.value -= 1

    def cover(self):

        self.top.remove_h()
        for row in self.top.loop("down"):
            for node in row.loop("right"):
                node.remove_v()

    def uncover(self):
        for row in self.top.loop("up"):
            for node in row.loop("left"):
                node.inse
