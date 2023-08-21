class Node:
    """Node class for graphalith"""
    def __init__(self, val = None, left = None, right = None) -> None:
        self.val = val
        self.left = left
        self.right = right

    def bfs(self):
        """Breadth first search for node class"""
        if self is None:
            return []
        
        ret = []
        queue = [self]
        while queue:
            node = queue.pop(0)
            ret.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return ret


