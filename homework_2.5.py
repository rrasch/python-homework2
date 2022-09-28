#!/usr/bin/python3

"""
    homework_2.5.py -- Build a JSON dict of dicts based on the revenue table

    Author: Rasan Rasch (rasan@nyu.edu)
    Last Revised: 9/28/2022
"""

import json
import os
import sqlite3


def convert_db_to_json(dbname, jsonfile):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    cur.execute("SELECT * from revenue")

    dod = {}

    for row in cur:
        company, state, cost = row
        dod[company] = {"name": company, "state": state, "amount": cost}

    conn.close()

    fh = open(jsonfile, "w")
    json.dump(dod, fh, indent=4)
    fh.close()


data_dir = os.path.join(
    os.environ["HOME"], "python_data_apy", "session_02_working_files"
)
db_name = os.path.join(data_dir, "session_2.db")
json_file = "revenue.json"

convert_db_to_json(db_name, json_file)

