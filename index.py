from flask import Flask
import utils

app = Flask(__name__)

@app.route("/")
def index():
    index = ""
    with open("html/index.html") as f:
        index = f.read()
    
    return index

if __name__ == "__main__":
    app.run()