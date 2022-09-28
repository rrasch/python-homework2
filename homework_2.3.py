#!/usr/bin/python3

"""
    homework_2.3.py -- read from weather_newyork.csv, select the date,
                       mean_temp, precip and events columns,
                       and insert them row-by-row into the table
                       weather_newyork

    Author: Rasan Rasch (rasan@nyu.edu)
    Last Revised: 9/28/2022
"""

import csv
import os
import sqlite3


def create_and_fill_weather_ny_table(dbname, csvfile):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS weather_newyork")
    conn.commit()

    cur.execute(
        """
        CREATE TABLE weather_newyork (
            date TEXT,
            mean_temp INT,
            precip FLOAT,
            events TEXT
        )
        """
    )
    conn.commit()

    query = "INSERT INTO weather_newyork VALUES (?, ?, ?, ?)"

    fh = open(csv_file)
    reader = csv.reader(fh)
    headers = next(reader)

    for fields in reader:
        date = fields[0]
        mean_temp = fields[1]
        precip = fields[-4]
        events = fields[-2]

        if precip == "T":
            precip = None

        cur.execute(query, [date, mean_temp, precip, events])
        conn.commit()

    fh.close()

    conn.close()


data_dir = os.path.join(
    os.environ["HOME"], "python_data_apy", "session_02_working_files"
)
db_name = os.path.join(data_dir, "session_2.db")
csv_file = os.path.join(data_dir, "weather_newyork.csv")

create_and_fill_weather_ny_table(db_name, csv_file)

