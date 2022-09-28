#!/usr/bin/python3

"""
    homework_2.2.py -- creates a new table called weather_newyork
                       in the session_2.db

    Author: Rasan Rasch (rasan@nyu.edu)
    Last Revised: 9/28/2022
"""

import os
import sqlite3


def create_weather_ny_table(dbname):
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

    conn.close()


db_name = os.path.join(
    os.environ["HOME"],
    "python_data_apy",
    "session_02_working_files",
    "session_2.db",
)

create_weather_ny_table(db_name)

