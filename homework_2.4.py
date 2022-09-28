#!/usr/bin/python3

"""
    homework_2.4.py -- read from weather_newyork_dod.json, select
                       the date, mean_temp, precip and events values
                       from each dict, and insert them row-by-row
                       into the table weather_newyork

    Author: Rasan Rasch (rasan@nyu.edu)
    Last Revised: 9/28/2022
"""

import json
import os
import sqlite3


def create_and_fill_weather_ny_table(dbname, jsonfile):
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

    fh = open(json_file)
    data = json.load(fh)
    fh.close()

    for date, fields in data.items():
        mean_temp = fields["mean_temp"]
        precip = fields["precip"]
        events = fields["events"]

        if precip == "T":
            precip = None

        cur.execute(query, [date, mean_temp, precip, events])
        conn.commit()

    conn.close()


data_dir = os.path.join(
    os.environ["HOME"], "python_data_apy", "session_02_working_files"
)
db_name = os.path.join(data_dir, "session_2.db")
json_file = os.path.join(data_dir, "weather_newyork_dod.json")

create_and_fill_weather_ny_table(db_name, json_file)

