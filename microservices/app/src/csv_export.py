import csv
import json, requests
from flask import jsonify


def csv_dict_reader(file_obj):
    total = 0; # total no of enteries
    fail = 0    # total number of failed entries
    list = []   # list to add JSON objects
    """
    Read a CSV file using csv.DictReader
    """

    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        total=total+1
        try:
            # If Any Value is missing
            if line["aadhar_no"]==None or line["mobile"]==None or line["comp_name"]==None or line['LSA']==None:
                fail=fail+1
            else:
                list.append({"aadhar_no": line["aadhar_no"], "mobile": line["mobile"], "comp_name": line["comp_name"],
                         "LSA": line['LSA']})
        except:
            fail=fail+1

    return list,fail,total


def csv_export(route_of_csv):
    with open("test.csv") as f_obj:
        list,fail,total=csv_dict_reader(f_obj)
        print list,fail,total

        url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
            "table": "central",
            "objects": list
        },
            "on_conflict": {
                "action": "ignore",
                "constraint": "mobile"
            }
        }

    # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        if 'error' in resp.json():
            return "Some mobile number is repeated plzz. check before entering"
        else:
            data={
                "total":total,
                "success":resp.json()['affected_rows'],
                "fail":total-resp.json()['affected_rows']
            }
            return (data)

print csv_export(route_of_csv="man.csv")




