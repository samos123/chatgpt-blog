import math

from flask import Flask, render_template, request, make_response
import markdown

from models import Entry, db


app = Flask(__name__)


@app.route("/")
def index():
    db.connect(True)
    num_pages = math.ceil(Entry.select().where(Entry.answer.is_null(False)).count() / 20)
    page = int(request.args.get("page", 1))
    entries = Entry.select(Entry.id, Entry.slug, Entry.title, Entry.created)\
        .where(Entry.answer.is_null(False)).order_by(Entry.created.desc()).paginate(page, 20)
    return render_template("index.html", entries=entries, num_pages=num_pages, current_page=page)


@app.route("/<int:post_id>-<string:path>")
def entry(post_id, path):
    db.connect(True)
    e = Entry.get_by_id(post_id)
    if e.answer:
        e.answer = markdown.markdown(e.answer, extensions=['fenced_code'])
    return render_template("entry.html", entry=e, title=e.title)


@app.route("/sitemap.xml")
def sitemap():
    pages = Entry.select(Entry.slug, Entry.created).where(Entry.answer.is_null(False))
    resp = make_response(render_template("sitemap.xml", pages=pages))
    resp.headers['Content-Type'] = 'application/xml'
    return resp


if __name__ == "__main__":
    app.run("127.0.0.1", 5050, debug=True)
