
class Node_label:
    label=0
    def __init__(self, value):
        self.label = Node_label.label
        Node_label.label+=1
        self.value = value
        self.childs = []
        self.father = -1
		
    def __repr__(self):
        return 'l=%d v=%d' % (self.label, self.value)

    def add_child(self, node):
        self.childs.append(node)

class Node_component:
    label=0
    def __init__(self, value):
        self.label = Node_component.label
        Node_component.label+=1
        self.original_value=value
        self.value = value
        self.area=0
        self.active=True
        self.childs = []
        self.father = -1
        self.pixels = []

    def __repr__(self):
        return 'l=%d - a=%d g=%s' % (self.label, self.area, self.value)

    def add_child(self, node):
        self.childs.append(node)