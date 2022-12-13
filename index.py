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
    return [name[0] for name in utils.search(searched)]


@app.route("/submit", methods=['POST'])
def submit():
    print("Value submitted")
    submitted = request.get_json(force=True)

    utils.update_database(submitted["chosen"], submitted['suggestions'])

    return jsonify({"status": "Ok"})


if __name__ == "__main__":
    app.run()
