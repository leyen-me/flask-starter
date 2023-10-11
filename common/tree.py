class Tree:

    # 扁平转树
    @classmethod
    def build_tree(cls, flat_data):
        # 创建一个字典，用于存储每个节点的ID作为键，节点对象作为值
        nodes_dict = {}
        # 创建根节点列表，用于存储根节点
        root_nodes = []
        # 第一次遍历，将每个节点对象存储到字典中
        for item in flat_data:
            item['children'] = []
            nodes_dict[item["id"]] = item
        # 第二次遍历，建立树结构
        for item in flat_data:
            node = nodes_dict[item["id"]]
            parent_id = item.get("pid")
            if parent_id is None:
                # 如果没有父节点ID，将当前节点视为根节点的子节点
                root_nodes.append(node)
            else:
                # 如果有父节点ID，将当前节点添加到父节点的children列表中
                parent_node = nodes_dict.get(parent_id)
                if parent_node:
                    parent_node["children"].append(node)
                else:
                    root_nodes.append(node)
        return root_nodes
    
    @classmethod
    def get_child_ids(cls, tree, target_id, result=None, target_id_isp = False):
        if result is None:
            result = []
        for item in tree:
            if(target_id_isp):
                result.append(item['id'])
            else:
                if item["id"] == target_id:
                    cls.get_child_ids(item["children"] , target_id, result, True)
                else:
                    cls.get_child_ids(item["children"] , target_id, result, target_id_isp)
        return result