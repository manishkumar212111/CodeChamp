import base64
import string,random,requests,json
def id_generator(size=11, chars=string.ascii_uppercase+string.ascii_lowercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))
def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = bytes(chr((ord(clear[i]) + ord(key_c)) % 256))
        enc.append(enc_c)

    return bytes(base64.b64encode("".join(enc)))

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)
p=id_generator()
key='fsf'
print encode(key,"bfjbsdj")
key="huheuhr3u4h3urieurw"
url = "https://data.despairing12.hasura-app.io/v1/query"

# This is the json payload for the query
requestPayload = {
    "type": "insert",
    "args": {
        "table": "login_ceredential",
        "objects": [
            {
                "username": "sdfshfjsf",
                "password": encode(key,p)
            }
        ]
    }
}

# Setting headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 4f3156a40c12394198aaa87dacd0b53ebf32d1d3ee4271b8"
}

# Make the query and store response in resp
#resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

# resp.content contains the json response.
#print resp.content



