import datetime
import os

from dotenv import load_dotenv
from peewee import *

load_dotenv()

from playhouse.db_url import connect

# Connect to the database URL defined in the environment, falling
# back to a local Sqlite database if no database URL is specified.
db = connect(os.environ.get('DATABASE') or 'sqlite:///test.db')

class Entry(Model):
    class Meta:
        database = db
    slug = CharField(unique=True)
    prompt = TextField()
    response = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)


if __name__ == "__main__":
    db.connect()
    db.create_tables([Entry])
