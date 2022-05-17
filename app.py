from flask import Flask, render_template, jsonify, request, redirect
import utils

app = Flask(__name__)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/search-id/", methods=["POST"])
def search():
    s = request.values.get("s")
    return redirect(f"/item/{s}/")


@app.route("/item/<itemid>/")
def item_page(itemid):
    animal = utils.get_animal(itemid)
    return render_template("item.html", itemid=itemid, animal=animal)


@app.route("/<itemid>/")
def item_json(itemid):
    animal = utils.get_animal(itemid)
    return jsonify(animal)


if __name__ == '__main__':
    app.run()
