#!/usr/bin/env python3

"""

    get_permits.py: Retruns permit information from the City of Raleigh Building Permit
                    open data portal for street addresses specified.
                    
    
    Todd Moughamer
    
    March 20, 2016          v 1.0.0     initial version

"""

"""
    TO DO:
    * convert upper case for addresses automatically
    * if service won't accept un-abbreviated street terms catch and convert common onces (e.g, Road to RD)
    * consider printing full record as JSON rather than Python as string form for full record
"""


import json
import requests
import pprint
import datetime
import argparse
import re

# globals
URI_STEM = "https://data.raleighnc.gov/resource/4d6n-2yak.json?address_address="

# set up argument parser
parser = argparse.ArgumentParser(description="Return a summary of City of Raleigh building permit data for a given address")
parser.add_argument("addresses", type=str, nargs='+', help="addresses to query for, quote each if mulitple, all caps")
parser.add_argument("--full", action="store_true", help="pretty print the full record for each address")
args = parser.parse_args()

# reformat address for inclusion in uri
addresses = []
for a in args.addresses:
    # replace spaces
    addresses.append(re.subn(r"\s","%20",a)[0])

# retrieve records for each address from the portal
records = []
for a in addresses:
    uri = URI_STEM+a
    http_call = requests.get(uri)
    records.append(http_call.text)

# display each record
for r in records:
    data = json.loads(r)
    for i in data:
        if args.full:
            # display the full records
            pprint.pprint(i)
        else:
            # display a tabular summary of each record
            date = datetime.datetime.strptime(i['issue_date'],"%Y-%m-%dT%H:%M:%S.%f")
            print("%s\t%s\t%s\t%s\t%s" % (i['permit_number'],i['address_address'],date,i['proposed_work'],i['land_use_code_description']))
