from flask import Flask, render_template
import markdown

from models import Entry, load_test_data


app = Flask(__name__)


@app.route("/")
def index():
    entries = Entry.select().order_by(Entry.created.desc()).limit(10)
    return render_template("index.html", entries=entries)


@app.route("/<int:post_id>-<string:path>")
def entry(post_id, path):
    e = Entry.get_by_id(post_id)
    if e.answer:
        e.answer = markdown.markdown(e.answer)
    return render_template("entry.html", entry=e)


if __name__ == "__main__":
    app.run("127.0.0.1", 5050, debug=True)