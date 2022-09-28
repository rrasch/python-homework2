#!/usr/bin/python3

"""
    homework_2.1.py -- reads from a table in an sqlite database,
                       and writes to a CSV file.

    Author: Rasan Rasch (rasan@nyu.edu)
    Last Revised: 9/27/2022
"""

import csv
import os
import sqlite3


def sql_to_csv(dbname, tbl_name, csv_fname):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    fh = open(csv_fname, "w", newline="")
    writer = csv.writer(fh)

    cur.execute(f"SELECT * from {tbl_name}")

    writer.writerow([col[0] for col in cur.description])

    for row in cur:
        writer.writerow(row)

    conn.close()
    fh.close()


db_name = os.path.join(
    os.environ["HOME"],
    "python_data_apy",
    "session_02_working_files",
    "session_2.db",
)
table_name = "revenue"
csv_filename = "revenue_from_db.csv"

sql_to_csv(db_name, table_name, csv_filename)

