#!/usr/bin/python3
import sqlite3

db_name = "SENSORS.db"
table_name = "SENSORS_TABLE"

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

#ROWID is an SQLite3 keyword
sql_sample_count = "SELECT COUNT(ROWID), DATETIME FROM " + table_name
cursor.execute(sql_sample_count)
for row in cursor:
        count = row[0]

sql_min_temp = "SELECT MIN(TEMPERATURE), DATETIME FROM " + table_name
sql_avg_temp = "SELECT AVG(TEMPERATURE) FROM " + table_name
sql_max_temp = "SELECT MAX(TEMPERATURE), DATETIME FROM " + table_name

sql_min_press = "SELECT MIN(PRESSURE), DATETIME FROM " + table_name
sql_avg_press = "SELECT AVG(PRESSURE) FROM " + table_name
sql_max_press = "SELECT MAX(PRESSURE), DATETIME FROM " + table_name

print("\n")
print("-----------TEMPERATURE Statistics of %d Samples-----------" % count)
cursor.execute(sql_min_temp)
for row in cursor:
	print("MINIMUM TEMPERATURE: " + str(format(row[0], '.2f')) + " degC" + " DATETIME: " + str(row[1]))

cursor.execute(sql_avg_temp)
for row in cursor:
	print("AVERAGE TEMPERATURE: " + str(format(row[0], '.2f')) + " degC")  

cursor.execute(sql_max_temp)
for row in cursor:
	print("MAXIMUM TEMPERATURE: " + str(format(row[0], '.2f')) + " degC" + " DATETIME: " + str(row[1]))

print("\n")
print("------------PRESSURE Statistics of %d Samples------------" % count)
cursor.execute(sql_min_press)
for row in cursor:
	print("MINIMUM PRESSURE: " + str(format(row[0], '.2f')) + " mbar" + " DATETIME: " + str(row[1]))

cursor.execute(sql_avg_press)
for row in cursor:
	print("AVERAGE PRESSURE: " + str(format(row[0], '.2f'))  + " mbar")

cursor.execute(sql_max_press)
for row in cursor:
	print("MAXIMUM PRESSURE: " + str(format(row[0], '.2f')) + " mbar" + " DATETIME: " + str(row[1]))

print("\n")
			
cursor.close()
conn.close()

