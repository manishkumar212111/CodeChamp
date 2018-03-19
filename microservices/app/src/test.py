import csv
import json,requests

def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    count=0;
    list = []
    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        try:
            list.append({"aadhar_no":line["aadhar_no"],"mobile":line["mobile"],"comp_name":line["comp_name"],"LSA":line['LSA']})
        except:
            print "hii"
        count=count+1;
    return list

with open("test.csv") as f_obj:
    print csv_dict_reader(f_obj)






