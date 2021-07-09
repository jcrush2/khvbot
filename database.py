import os

import peewee as pw
from playhouse.db_url import connect

from logger import db_log

# Удалить в будущем

# Магия монтажа. Peewee не умеет (26.06.2019) принимать в себя адрес базы одной
# строкой, так что приходится парсить вручную.
# DB_ADDRESS = os.environ["DATABASE_URL"]
# db_log.info(f"Database address: {DB_ADDRESS}")
#
# DB_ADDRESS = DB_ADDRESS.replace("postgres://", "")
#
# splitters = [":", "@", ":", "/", " "]
# database_data = []
# for split in splitters:
# 	database_data.append(DB_ADDRESS.split(split, maxsplit=1)[0])
# 	DB_ADDRESS = DB_ADDRESS.replace(database_data[-1] + split, "")
#
# db_log.info(f"Connecting param: {database_data}")
# user, password, host, port, database_name = database_data
#
#
# db = pw.PostgresqlDatabase(database_name,
# 	user=user,
# 	host=host,
# 	password=password,
# 	port=port)
#
#
# # db = pw.PostgresqlDatabase(DATABASE_ADDRESS, autocommit=True)

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


class Users(BaseModel):
	userid = pw.IntegerField(null=False)
