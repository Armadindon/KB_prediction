from flask import Flask, request, jsonify
import utils

app = Flask(__name__)

@app.route("/")
def index():
    index = ""
    with open("html/index.html") as f:
        index = f.read()
    
    return index

@app.route("/search")
def search():
    searched = request.args.get("search")
    return utils.search(searched)

if __name__ == "__main__":
    app.run()