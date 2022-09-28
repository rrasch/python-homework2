#!/usr/bin/python3

"""
    homework_2.6.py -- Read the ip_routes.json file into a Python object,
                       provide code that can answer three questions

    Author: Rasan Rasch (rasan@nyu.edu)
    Last Revised: 9/27/2022
"""

import json
import os
import pprint


data_dir = os.path.join(
    os.environ["HOME"], "python_data_apy", "session_02_working_files"
)
json_file = os.path.join(data_dir, "ip_routes.json")

fh = open(json_file)
data = json.load(fh)
fh.close()

routes = data["result"][0]["vrfs"]["default"]["routes"]

print(f"number of keys in the 'routes' dict: {len(routes.keys())}")

print("\nips with a 'routeType' of 'iBGP'")
for ip, attr in routes.items():
    if attr["routeType"] == "iBGP":
        print(ip)

print("\nkeys other than 'routes' in the 'default' dict")
default_dict = data["result"][0]["vrfs"]["default"]
for key in default_dict.keys():
    if key != "routes":
        print(key)

