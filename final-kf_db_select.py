#!/usr/bin/python3
import sqlite3

db_name = "SENSORS.db"
table_name = "SENSORS_TABLE"

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

#ROWID is an SQLite3 keyword
sql_read = "SELECT ROWID, * FROM " + table_name
cursor.execute(sql_read)

for row in cursor:
    #print(row)
    record = "{ Unique_Sample_ID: " + str(row[0]) + ", "
    record += "SENSOR_ID: " + str(row[1]) + ", "
    record += "TEMPERATURE: " + str(format(row[2], '.2f')) + " degC, "
    record += "PRESSURE: " + str(format(row[3], '.2f')) + " mbar, "
    record += "DATETIME: " + str(row[4]) + " }"
    print(record)
    
cursor.close()
conn.close()

