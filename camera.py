import cv2
import numpy as np

# Load YOLO model
yolo_config = "yolo-cfg/yolov4.cfg"  # Change to yolov3.cfg if using YOLOv3
# Change to yolov3.weights if using YOLOv3
yolo_weights = "yolo-cfg/yolov4.weights"
yolo_names = "yolo-cfg/coco.names"

# Load class labels
with open(yolo_names, "r") as f:
    class_names = f.read().strip().split("\n")

# Load YOLO model
net = cv2.dnn.readNet(yolo_weights, yolo_config)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # Use GPU if available

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]

    # Convert frame to blob format for YOLO
    blob = cv2.dnn.blobFromImage(
        frame, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and class_names[class_id] == "person":
                # Get bounding box coordinates
                center_x, center_y, w, h = (
                    detection[:4] * np.array([width, height, width, height])).astype("int")
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression (NMS) to remove redundant boxes
    indexes = cv2.dnn.NMSBoxes(
        boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = f"Person: {confidences[i]:.2f}"
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("YOLO Person Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
