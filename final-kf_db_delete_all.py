#!/usr/bin/python3
import sqlite3
import os

db_name = "SENSORS.db"
table_name = "SENSORS_TABLE"

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

#ROWID is an SQLite3 keyword
sql_remove = "DELETE FROM {0};".format(table_name)
cursor.execute(sql_remove)

conn.commit()
cursor.close()
conn.close()

os.remove('SENSORS_LOG.txt')
