
class System:
    def __init__(self, boxes):
        self.boxes = boxes

    def advance(self):
        for box in self.boxes:
            box.concentration += 0


class Box:
    def __init__(self, name, inputs, outputs, generation_term=0):
        self.inputs = inputs
        self.outputs = outputs
        self.name = name
        self.concentration = 0


box_1 = Box("box1", {"box3": 1}, {"box2": 1})
box_2 = Box("box2", {"box1": 1}, {"box3": 1})
box_3 = Box("box3", {"box2": 1}, {"box1": 1})
