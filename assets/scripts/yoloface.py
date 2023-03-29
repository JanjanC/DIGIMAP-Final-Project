import numpy as np
import cv2
from PIL import Image
import io
from base64 import b64encode


class YOLOFace:
    def __init__(self, weight_path, cfg_path):
        self.yolo_net = cv2.dnn.readNet(weight_path, cfg_path)

    def detect(self, image_path=None, frame_status=False, frame_list=None):
        self.image_path = image_path
        self.frame_status = frame_status
        self.frame_list = frame_list

        if self.image_path != None and self.frame_status == False and self.frame_list == None:
            self.image_path = image_path
            img = cv2.imread(self.image_path)
        else:
            img = self.frame_list

        height, width, _ = img.shape
        blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

        self.yolo_net.setInput(blob)
        output_layers = self.yolo_net.getUnconnectedOutLayersNames()
        output_list = self.yolo_net.forward(output_layers)

        boxes = []
        confidences = []
        class_ids = []

        for output in output_list:
            for detection in output:
                confidence = detection[5]  # only one class (face)
                if confidence > 0.50:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - (w / 2))
                    y = int(center_y - (h / 2))
                    boxes.append([x, y, h, w])
                    confidences.append((float(confidence)))
                    class_ids.append(0)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.5)
        face_box = []
        face_confidence = []

        if len(indexes) > 0:
            for i in indexes.flatten():
                face_box.append(boxes[i])
                face_confidence.append(confidences[i])

        return img, face_box, face_confidence

    def show(self, img, face_box, frame_status=False):
        self.img = img
        self.face_box = face_box
        self.frame_status = frame_status

        if len(face_box) > 0:
            for i in range(len(face_box)):
                box = face_box[i]
                x, y, w, h = box[0], box[1], box[2], box[3]
                cv2.rectangle(self.img, (x, y), (x + h, y + w), (255, 255, 255), 1)

        if self.frame_status == False:
            img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)  # Converting BGR to RGB
            img = Image.fromarray(img)
            file_object = io.BytesIO()
            img.save(file_object, 'PNG')
            base64img = "data:image/png;base64," + b64encode(file_object.getvalue()).decode('ascii')
            return base64img
        else:
            img_output = self.img
            return img_output
