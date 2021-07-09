import os

import peewee as pw
from playhouse.db_url import connect

from logger import db_log


DB_ADDRESS = os.environ["DATABASE_URL"]
db = connect(DB_ADDRESS)

db_log.debug(f"Create database with address {DB_ADDRESS}")

# В запросах в програме использованы логические
# операторы поскольку (из документации Peewee):
# Peewee uses bitwise operators (& and |)
# rather than logical operators (and and or)

# Postgres database -+


class BaseModel(pw.Model):

	class Meta:
		database = db


class User(BaseModel):
	userid = pw.IntegerField(null=False)

	class Meta:
		db_table = "users"
		primary_key = pw.CompositeKey("userid")
