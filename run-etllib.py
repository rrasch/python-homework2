#!/usr/bin/python3

"""
    homework_2.7.py -- Write a module called etllib.py with the following
                       four functions for performing four transforms:
                       SQL->CSV, SQL->JSON, CSV->SQL, JSON->SQL.

    Author: Rasan Rasch (rasan@nyu.edu)
    Last Revised: 9/28/2022
"""

from etllib import sql2csv, sql2json, csv2sql, json2sql
import os
import shutil
import sqlite3


data_dir = os.path.join(
    os.environ["HOME"], "python_data_apy", "session_02_working_files"
)

orig_db_name = os.path.join(data_dir, "session_2.db")
db_name = "my.db"
shutil.copy(orig_db_name, db_name)  # work with my own copy of sessions_2.db
csv_file = os.path.join(data_dir, "weather_newyork.csv")
json_file = os.path.join(data_dir, "weather_newyork_dod.json")

conn = sqlite3.connect(db_name)

csv2sql(csv_file, conn, "hw_weather_newyork")

query = "SELECT date, max_dewpoint, max_sealevel FROM hw_weather_newyork"

with open("sql2csv.csv", "w") as fh:
    fh.write(sql2csv(query, conn))

with open("sql2json.json", "w") as fh:
    fh.write(sql2json(query, conn, format="dod", primary_key="max_sealevel"))

json2sql(json_file, conn, "weather_newyork_dod")

conn.close()

