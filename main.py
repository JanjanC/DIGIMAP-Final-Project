import os
from flask import Flask, render_template
from assets.scripts.yoloface import YOLOFace

app = Flask(__name__, template_folder=os.path.join("assets", "templates"), static_folder="assets")
model = YOLOFace(os.path.join(os.getcwd(), "assets", "model", "face_detection.cfg"), os.path.join(os.getcwd(), "assets", "model", "face_detection.weights"))


@app.route("/")
def hello_world():
    img_path = os.path.join(os.getcwd(), "assets", "images", "image.png")
    img, box, confidence = model.detect(img_path)
    output = model.show(img, box)

    return render_template("index.html", base64img=output)

if __name__ == "__main__":
    app.run(debug=True)
