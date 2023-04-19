import os
import cv2
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from assets.scripts.yoloface import YOLOFace

UPLOAD_FOLDER = os.path.join("assets", "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__, template_folder=os.path.join("assets", "templates"), static_folder="assets")

model = YOLOFace(os.path.join(os.getcwd(), "assets", "model", "yolo_face_tiny.cfg"), os.path.join(os.getcwd(), "assets", "model", "yolo_face_tiny.weights"))

app.secret_key = "secretkey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")


# a function to check if the file extension is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/results', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'filepond' not in request.files:
        return render_template("index.html", error="Failed to Upload File")
    file = request.files['filepond']

    # if the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        return render_template("index.html", error="No Valid File Uploaded")
    
    # invalid file extension
    if not allowed_file(file.filename):
        return render_template("index.html", error="Invalid File Type")
    
    # a valid file was uploaded
    if file:
        filename = secure_filename(file.filename)
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(img_path)
        # run face detection
        img, box, confidence = model.detect(img_path)
        input_img = model.convert_img(img) # convert input image to base64
        output = model.show_box(img, box) # draw bounding box
        output_img = model.convert_img(output) # convert output image to base64
        if os.path.isfile(img_path):
            os.remove(img_path)
        return render_template("result.html", input_img=input_img, output_img=output_img)


if __name__ == "__main__":
    app.run()
