import datetime
import os
import sys

from dotenv import load_dotenv
from peewee import *
from playhouse.db_url import connect
import requests
from slugify import slugify

load_dotenv()


# Connect to the database URL defined in the environment, falling
# back to a local Sqlite database if no database URL is specified.
db = connect(os.environ.get('DATABASE') or 'sqlite:///test.db')


class Entry(Model):
    class Meta:
        database = db
    slug = TextField()
    prompt = TextField()
    title = TextField()
    answer = TextField(null=True)
    question_id = IntegerField(null=True)
    question_body = TextField()
    created = DateTimeField(default=datetime.datetime.now)


def load_test_data():
    Entry.delete()
    questions = requests.get("https://api.stackexchange.com/2.3/questions?fromdate=1670630400&"
                             "order=desc&max=1670716800&sort=activity&tagged=golang&site=stackoverflow"
                             "&filter=!nOedRLbBQj").json()
    for item in questions["items"]:
        prompt = item["title"] + "<br/>" + item["body"]
        Entry.get_or_create(slug=slugify(item["title"]), prompt=prompt,
                            question_id=item["question_id"], question_body=item["body"], title=item["title"])


if __name__ == "__main__":
    if sys.argv[1] == "create_tables":
        db.connect()
        db.create_tables([Entry])
    if sys.argv[1] == "load_test_data":
        load_test_data()
    if sys.argv[1] == "delete_all_data":
        Entry.delete()
