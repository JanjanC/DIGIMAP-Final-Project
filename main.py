import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from assets.scripts.yoloface import YOLOFace

UPLOAD_FOLDER = os.path.join("assets", "uploads")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder=os.path.join("assets", "templates"), static_folder="assets")
app.secret_key = "secretkey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = YOLOFace(os.path.join(os.getcwd(), "assets", "model", "yolo_face.cfg"), os.path.join(os.getcwd(), "assets", "model", "yolo_face.weights"))

@app.route("/")
def index():
    img_path = os.path.join(os.getcwd(), "assets", "images", "image.png")
    img, box, confidence = model.detect(img_path)
    output = model.show(img, box)

    return render_template("index.html", base64img=output)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/submit', methods=['GET', 'POST'])
def upload_file():
    print(request.files)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'filepond' not in request.files:
            print('No file part')
            return redirect("/")
        file = request.files['filepond']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        print(type(file.stream))
        if file.filename == '':
            print('No selected file')
            return redirect("/")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/")

#  pass

if __name__ == "__main__":
    app.run(debug=True)
