import datetime
import logging
import os
import sys

from peewee import *
from playhouse.db_url import connect
import requests
from slugify import slugify

from utils import load_json_file

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
    question_date = DateTimeField(null=True)
    created = DateTimeField(default=datetime.datetime.now)

    def question_url(self):
        return f"https://stackoverflow.com/q/{self.question_id}"

    def generate_answer(self, chatbot):
        if not self.id:
            raise Exception("Can only generate answer on existing records")
        response = chatbot.ask(self.prompt)
        self.answer = response.get("message")
        self.save()


def load_so_data(fromdate: datetime.datetime, todate: datetime.datetime):
    fromts = int(fromdate.timestamp())
    maxts = int(todate.timestamp())
    url = (f"https://api.stackexchange.com/2.3/questions?fromdate={fromts}&max={maxts}"
           "&order=desc&sort=activity&tagged=golang&site=stackoverflow&filter=!nOedRLbBQj")
    questions = requests.get(url).json()
    entries = []
    for item in questions["items"]:
        prompt = item["title"] + "<br/>" + item["body"] + " ".join(item["tags"])
        question_date = datetime.datetime.utcfromtimestamp(item["creation_date"])
        entries.append(Entry.get_or_create(slug=slugify(item["title"]), prompt=prompt, question_date=question_date,
                            question_id=item["question_id"], question_body=item["body"], title=item["title"]))
    return entries


if __name__ == "__main__":
    if sys.argv[1] == "create_tables":
        db.connect()
        db.create_tables([Entry], safe=True)
    if sys.argv[1] == "load_test_data":
        fromdate = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d")
        todate = datetime.datetime.strptime(sys.argv[3], "%Y-%m-%d")
        entries = load_so_data(fromdate, todate)
        print(f"Loaded {len(entries)} into the database")
    if sys.argv[1] == "delete_all_data":
        Entry.delete()
    if sys.argv[1] == "generate_answer":
        from revChatGPT.ChatGPT import Chatbot
        chatbot = Chatbot(load_json_file("chatgpt.json"), conversation_id=None)
        entry_id = int(sys.argv[2])
        entry = Entry.get_by_id(entry_id)
        entry.generate_answer(chatbot)
    if sys.argv[1] == "generate_answers":
        from revChatGPT.ChatGPT import Chatbot
        chatbot = Chatbot(load_json_file("chatgpt.json"), conversation_id=None)
        entries = Entry.select().where(Entry.answer.is_null())
        for entry in entries:
            try:
                print(f"Generating answer for: {entry.id} - {entry.title}")
                print(entry.id)
                entry.generate_answer(chatbot)
            except:
                logging.exception("error while generating answer")
