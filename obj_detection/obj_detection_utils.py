import numpy as np

class InferedDetections:
    def __init__(self, image, num_detections, boxes, classes, scores, masks = None, is_normalized = True, get_category_fnc=None, anotator=None):
        self.num_detections = int(np.squeeze(num_detections))
        self.image = image
        self.height, self.width = image.shape[0], image.shape[1]
        if is_normalized:
            self.boxes_normalized = boxes
            self.boxes = boxes * [self.height, self.width, self.height, self.width]
        else:
            self.boxes_normalized = boxes / [self.height, self.width, self.height, self.width]
            self.boxes = boxes
        self.classes = classes
        self.scores = scores
        self.masks = masks
        self.boxes_as_xywh = None
        self.get_category_fnc=get_category_fnc
        self.anotator = anotator

    def get_scores(self, index = None):
        if index:
            return self.scores[index]
        else:
            return self.scores

    def get_classes(self, index = None):
        if index:
            return self.classes[index]
        else:
            return self.classes

    def get_boxes_tlbr(self, index = None, normalized = True):
        if normalized:
            boxes = self.boxes_normalized
        else:
            boxes = self.boxes
        if index:
            return boxes[index]
        else:
            return boxes

    def get_masks(self, index = None):
        if index:
            return self.masks[index]
        else:
            return self.masks

    def get_image(self):
        return self.image

    def get_boxes_as_xywh(self):
        if self.boxes_as_xywh is None:
            self.boxes_as_xywh = []
            for i in range(self.num_detections):
                self.boxes_as_xywh.append([self.boxes[i][1], self.boxes[i][0],
                                           self.boxes[i][3] - self.boxes[i][1],
                                           self.boxes[i][2] - self.boxes[i][0]])
            self.boxes_as_xywh = np.array(self.boxes_as_xywh)
        return self.boxes_as_xywh

    def get_num_detections(self):
        return self.num_detections

    def get_category(self, category):
        return self.get_category_fnc(category)

    def anotate(self):
        return self.anotator(self)