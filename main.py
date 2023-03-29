import os
from flask import Flask, render_template

app = Flask(__name__, template_folder=os.path.join("assets", "templates"), static_folder="assets")


@app.route("/")
def hello_world():
    return render_template("index.html")


#  pass

if __name__ == "__main__":
    app.run(debug=True)
