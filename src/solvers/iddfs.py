"""
    IDDFS:
        Iterative Deepening Depth First Search
    This is a well known search algorithm
    It works by performing a DFS with limited depth
    The depth is first limited to 0 and  if DFS doesn't find a solution then the maximum depth is increased by 1

    Parameters:
        - start_node: node to start searching from
        - goal_test: a function that should take nodes as input and return True/False depending on if the node
            is the goal node
        - get_children: a function that should take nodes as input and return an iterable of the child nodes from the
            given node
        - min_depth: minimum depth at which the goal states can be found
        - depth_limit: maximum depth for the algorithm

    Returns:
        A pair (goal_node, depth_of_goal_node)

    Notes:
        The path from the start_node to the goal_node should be retrieved
            from the goal_node, this means that the get_children function should leave a pointer on each child node to
            its parent node
"""


def iddfs(start_node, goal_test, get_children, min_depth=0, depth_limit=int(1e6)):
    for depth in range(min_depth, depth_limit):
        print(depth)
        dfs_stack = [(start_node, 0)]

        while dfs_stack:
            node, d = dfs_stack.pop()
            if d < depth:
                for child in get_children(node):
                    dfs_stack.append((child, d+1))
            else:
                if goal_test(node):
                    return node, d
