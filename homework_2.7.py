#!/usr/bin/python

"""
    homework_2.7.py -- Write a module called etllib.py with the following
                       four functions for performing four transforms:
                       SQL->CSV, SQL->JSON, CSV->SQL, JSON->SQL.

    Author: Rasan Rasch (rasan@nyu.edu)
    Last Revised: 9/27/2022
"""

import csv
import json
import io
import os
import shutil
import sqlite3


def sql2csv(query, conn):
    """
    query a database and return string data in CSV format

    Arguments:  query   string SQL query to select data
                conn    database connection object

    Return Value:  a string with CSV-formatted data

    (note:  to return CSV data as a string, the csv writer
     must be given a StringIO object instead of an
     open file object.  See the io module for
     details)

    """

    cur = conn.cursor()
    print(query)
    cur.execute(query)

    headers = [col[0] for col in cur.description]

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(headers)
    for row in cur:
        writer.writerow(row)

    return output.getvalue()


def sql2json(query, conn, format='lod', primary_key=None):
    """
    query a database and return a JSON string

    if format is 'lod', function will return a
    list of dicts

    (If format is 'lod' and primary_key is specified,
     function should raise ValueError with a suitable
     message.)

    if format is 'dod', function will return a dict
    of dicts with the designated primary_key as
    "outer" dict key

    (If format is 'dod' and primary_key is not specified,
     function should raise ValueError with a suitable
     message.)

    Arguments:  query   string SQL query to select data
                conn    database connection object

                format (optional):
                        'lod' (list of dicts, the default) or
                        'dod' (dict of dicts)

                primary_key  (optional):
                        column value to use as the key
                        for a dict of dicts

                (note that if format == 'dod' then 'primary_key'
                 must be an existing column name;
                 if format == 'lod' then 'primary_key'
                 must be None -- use 'is None' or 'is not None'
                 to test)

    Raises:  ValueError if format is 'dod' and primary_key is
             not specified, or format is 'lod' and primary_key
             is specified.

    Return Value:  string in JSON format

    (note:  to return a JSON string rather than
     writing to a file, use the json.dumps()
     method, which returns a string, instead of
     the json.dump() method)

    """

    if format not in ['lod', 'dod']:
        raise ValueError(f"Invalid format '{format}'. Must be 'lod' or 'dod'")

    want_list = format == 'lod'

    if want_list and primary_key is not None:
        raise ValueError("Can't specify primary_key with format set to 'lod'")

    if not want_list and primary_key is None:
        raise ValueError("Must specifiy primary_key with format set to 'dod'")

    cur = conn.cursor()
    print(query)
    cur.execute(query)

    headers = [col[0] for col in cur.description]

    if not want_list and primary_key not in headers:
        raise ValueError(f"primary_key '{primary_key}' not found in query data")

    if want_list:
        data = []
    else:
        data = {}

    if not want_list:
        primary_key_index = headers.index(primary_key)

    for row in cur:
        fields = {}
        for i, val in enumerate(row):
            fields[headers[i]] = val
        if want_list:
            data.append(fields)
        else:
            data[row[primary_key_index]] = fields

    output = io.StringIO()
    json.dump(data, output, indent=4)
    return output.getvalue()


def csv2sql(filename, conn, table):
    """
    insert a csv file into a database table

    Arguments:  filename   CSV filename to read
                conn       database connection object
                table      table to insert to

    Return Value:  None (writes to database)
    """

    fh = open(filename)
    reader = csv.reader(fh)
    headers = next(reader)

    cur = conn.cursor()

    cur.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()

    columns = ', '.join([col + " TEXT" for col in headers])
    query = f"CREATE TABLE {table} ({columns})"
    print(query)
    cur.execute(query)
    conn.commit()

    val_placeholders = ', '.join(list('?' * len(headers)))
    query = f"INSERT INTO {table} VALUES ({val_placeholders})"

    for fields in reader:
        cur.execute(query, fields)
        conn.commit()
    fh.close()



def json2sql(filename, conn, table):
    """
    insert JSON data into a database

    Arguments:  filename   JSON file to read (assumes dict of dicts)
                           also assumes that "inner" dicts all have
                           identical keys
                conn       database connection object
                table      name of table to write to

    Return Value:  None (writes to database)
    """
    return None


data_dir = os.path.join(
    os.environ["HOME"], "python_data_apy", "session_02_working_files"
)

orig_db_name = os.path.join(data_dir, "session_2.db")
db_name = "my.db"
shutil.copy(orig_db_name, db_name)

conn = sqlite3.connect(db_name)

csv_file = os.path.join(data_dir, "weather_newyork.csv")

csv2sql(csv_file, conn, "hw_weather_newyork")

query = "SELECT date, max_dewpoint, max_sealevel FROM hw_weather_newyork"

print(sql2csv(query, conn))

print(sql2json(query, conn, format='dod', primary_key='max_sealevel'))

conn.close()

