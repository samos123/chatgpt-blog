from flask import Flask, render_template

from models import Entry, load_test_data


app = Flask(__name__)


@app.route("/")
def index():
    entries = Entry.select().order_by(Entry.created.desc()).limit(10)
    return render_template("index.html", entries=entries)


@app.route("/<int:post_id>-<string:path>")
def entry(post_id, path):
    entry = Entry.get_by_id(post_id)
    return render_template("entry.html", entry=entry)


if __name__ == "__main__":
    app.run("127.0.0.1", 5050, debug=True)