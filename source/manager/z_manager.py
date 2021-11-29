from copy import copy


class ZManager:
    def __init__(self, parent_node):
        self._parent = parent_node
        self._node_list = [elem[1] for elem in self._parent.children]
        self._default_list = copy(self._node_list)

        self._top = None
        self._bottom = None

        self._refresh()

    def _refresh(self):
        self.clear()
        self.assemble()

    def _obj_or_idx(self, target):
        if target in range(len(self._default_list)):
            return self._default_list[target]
        else:
            return target

    def get_parent(self):
        return self._parent

    def get_nodes(self):
        return self._node_list

    def set_nodes(self, nodes):
        self._node_list = nodes
        self._refresh()

    def clear(self):
        for node in self._node_list:
            self._parent.remove(node)
        self._top = 0
        self._bottom = -1

    def assemble(self):
        for node in self._node_list:
            self.add(node)
        self._top = len(self._node_list)

    def add(self, node, from_top=True):
        if from_top:
            z_order = self._top
        else:
            z_order = self._bottom

        self._parent.add(node, z=z_order)
        if node not in self._node_list:
            self._node_list.append(node)

        # Iteration
        if from_top:
            self._top += 1
        else:
            self._bottom -= 1

    def remove(self, node):
        self._parent.remove(node)
        self._node_list.remove(node)

    def set_top(self, target):
        target = self._obj_or_idx(target)
        self.remove(target)
        self.add(target)

    def set_bottom(self, target):
        target = self._obj_or_idx(target)
        self.remove(target)
        self.add(target, from_top=False)

    def do(self, action, target=None):
        if target is None:
            for node in self._node_list:
                node.do(action)
        else:
            target = self._obj_or_idx(target)
            target.do(action)

    def stop(self, target=None):
        if target is None:
            for node in self._node_list:
                node.stop()
        else:
            target = self._obj_or_idx(target)
            target.stop()
