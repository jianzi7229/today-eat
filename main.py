class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def build_tree_from_array(tree_array, root, index, total_nodes):
    if index < total_nodes:
        if tree_array[index] is None:
            return None

        root = TreeNode(tree_array[index])

        root.left = build_tree_from_array(tree_array, root.left, 2 * index + 1, total_nodes)
        root.right = build_tree_from_array(tree_array, root.right, 2 * index + 2, total_nodes)

    return root


def convert_to_linked_list(root):
    if root is None:
        return None

    queue = [root]
    linked_list = []

    while queue:
        node = queue.pop(0)
        linked_list.append(node)

        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)

    for i in range(len(linked_list) - 1):
        linked_list[i].right = linked_list[i + 1]

    return linked_list[0]


def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.data, end=" ")
        inorder_traversal(root.right)


# 主函数
def main():
    # 通过键盘输入建立设定的完全二叉树的顺序存储结构，这里使用示例数据
    tree_array = [1, 2, 3, 4, 5, 6, 7]

    # 将顺序结构的二叉树转化为链式结构
    root = None
    root = build_tree_from_array(tree_array, root, 0, len(tree_array))

    # 对给定二叉树进行中序遍历，显示遍历结果
    print("中序遍历结果:")
    inorder_traversal(root)


if __name__ == "__main__":
    main()
