import os
import cv2

print('Hello from python')

full_weight_path='face_detection.weights'
full_cfg_path='face_detection.cfg'

full_net = cv2.dnn.readNet(full_weight_path, full_cfg_path)

def face_detection(image_path=None, frame_status=False, frame_arr=None):
    
    image_path=image_path
    frame_status=frame_status
    frame_arr=frame_arr
    
    if image_path!=None and frame_status==False and frame_arr==None:         
        image_path=image_path
        img=cv2.imread(image_path)
    else:
        img=frame_arr    

    height,width, _ = img.shape      
    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
    
    full_net.setInput(blob)
    output_layers_names = full_net.getUnconnectedOutLayersNames()
    layerOutputs =full_net.forward(output_layers_names)
    classes=['face','back']
    
    boxes = []
    confidences = []
    class_ids = []
    
    for output in layerOutputs:
      for detection in output:
          scores = detection[5:]
          class_id = np.argmax(scores)
          confidence = scores[class_id]
          if confidence > 0.50:
              center_x = int(detection[0]*width)
              center_y = int(detection[1]*height)
              w= int(detection[2]*width)
              h= int(detection[3]*height)
              x = int(center_x - (w/2))
              y = int(center_y - (h/2))
              boxes.append([x, y,h, w])
              confidences.append((float(confidence)))
              class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    face_box=[]
    conf=[] 
    if len(indexes)>0:
        for i in indexes.flatten():
            label = str(classes[class_ids[i]])
            if label==classes[0]:
                face_box.append( boxes[i])
                conf.append(confidences[i])
    return img,face_box,conf  
   