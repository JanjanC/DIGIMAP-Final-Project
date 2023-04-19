import numpy as np
import cv2
from PIL import Image
import io
from base64 import b64encode


class YOLOFace:
    # load weight and cfg for the model
    def __init__(self, weight_path, cfg_path):
        self.yolo_net = cv2.dnn.readNet(weight_path, cfg_path)

    # detect the faces in the input image
    def detect(self, image_path):
        self.image_path = image_path
        
        # read image
        img = cv2.imread(self.image_path)
        
        height, width, _ = img.shape

        # preprocess image to 416x416
        blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

        # predict model output
        self.yolo_net.setInput(blob)
        output_layers = self.yolo_net.getUnconnectedOutLayersNames()
        output_list = self.yolo_net.forward(output_layers)

        boxes = []
        confidences = []

        # get the bounding boxes and confidence
        for output in output_list:
            for detection in output:
                confidence = detection[5]  # only one class (face)
                if confidence > 0.50: #score threshold of 0.5
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - (w / 2))
                    y = int(center_y - (h / 2))
                    boxes.append([x, y, h, w])
                    confidences.append((float(confidence)))

        # score threshold of 0.5 and nms threshold of 0.5
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        face_box = []
        face_confidence = []

        if len(indexes) > 0:
            for i in indexes.flatten():
                face_box.append(boxes[i])
                face_confidence.append(confidences[i])

        return img, face_box, face_confidence

    # draw a bounding box on the image
    def show_box(self, img, face_box):
        self.img = img
        self.face_box = face_box

        if len(face_box) > 0:
            for i in range(len(face_box)):
                box = face_box[i]
                x, y, w, h = box[0], box[1], box[2], box[3]
                cv2.rectangle(self.img, (x, y), (x + h, y + w), (255, 255, 255), 3)

        return img
    
    # convert image to base64
    def convert_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        file_object = io.BytesIO()
        img.save(file_object, 'PNG')
        img = "data:image/png;base64," + b64encode(file_object.getvalue()).decode('ascii')
        return img

