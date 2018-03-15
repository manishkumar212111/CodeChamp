import json,requests
import binascii,base64
from app import app
def b64encode(s, altchars=None):
   encoded = binascii.b2a_base64(s)[:-1]
   if altchars is not None:
      return (encoded, {'+': altchars[0], '/': altchars[1]})
   return encoded
def b64decode(s, altchars=None):
   if altchars is not None:
      s = (s, {altchars[0]: '+', altchars[1]: '/'})
   try:
      return binascii.a2b_base64(s)
   except:
       return False


def login(username,password):
    p1 = str.encode(password)
    pas = b64encode(p1)

    url = "https://data.despairing12.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "login_ceredential",
            "columns": [
                "username"
            ],
            "where": {
                "$and": [
                    {
                        "username": {
                            "$eq": username
                        }
                    },
                    {
                        "password": {
                            "$eq": json.dumps(pas.decode('utf-8'))
                        }
                    }
                ]
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    return resp.content