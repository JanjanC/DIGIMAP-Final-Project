import os
import cv2
from flask import Flask, Response, render_template, request, redirect
from werkzeug.utils import secure_filename
from assets.scripts.yoloface import YOLOFace

UPLOAD_FOLDER = os.path.join("assets", "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__, template_folder=os.path.join("assets", "templates"), static_folder="assets")

camera = cv2.VideoCapture(1)
model = YOLOFace(os.path.join(os.getcwd(), "assets", "model", "yolo_face_tiny.cfg"), os.path.join(os.getcwd(), "assets", "model", "yolo_face_tiny.weights"))

app.secret_key = "secretkey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# openCvVidCapIds = []

# for i in range(100):
#     try:
#         cap = cv2.VideoCapture(i)
#         if cap is not None and cap.isOpened():
#             openCvVidCapIds.append(i)
#         # end if
#     except:
#         pass
#     # end try
# # end for

# print(openCvVidCapIds)


@app.route("/")
def index():
    return render_template("index.html")


def generate_frames():
    while True:
        success, frame = camera.read()  # read the camera frame

        if not success:
            break
        else:
            _, box, _ = model.detect(frame_list=frame, frame_status=True)
            frame = model.show(frame, box, frame_status=True)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/submit', methods=['POST'])
def upload_file():
    print(request.files)
    # check if the post request has the file part
    if 'filepond' not in request.files:
        return render_template("index.html", error="Failed to upload file")
    file = request.files['filepond']
    # If the user does not select a file, the browser submits an empty file without a filename.
    print(type(file.stream))
    if file.filename == '':
        print('No selected file')
        return render_template("index.html", error="No valid file uploaded")
    if not allowed_file(file.filename):
        print('Invalid file type')
        return render_template("index.html", error="Invalid file type")
    if file:
        filename = secure_filename(file.filename)
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(img_path)
        img, box, confidence = model.detect(img_path)
        output = model.show(img, box)
        if os.path.isfile(img_path):
            os.remove(img_path)
        return render_template("index.html", base64img=output)


if __name__ == "__main__":
    app.run()
