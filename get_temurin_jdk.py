import argparse
import json
import ssl
import urllib

from http import client

HOST = "https://api.adoptium.net/v3/assets/latest/11/hotspot?release=latest&jvm_impl=hotspot&vendor=adoptium"

query_params = {
    "release": "latest",
    "jvm_impl": "hotspot",
    "vendor": "adoptium",
}

p = urllib.parse.urlencode(query_params)

connection = client.HTTPSConnection("api.adoptium.net", context=ssl._create_unverified_context())
connection.request("GET", "/v3/assets/latest/11/hotspot?release=latest&jvm_impl=hotspot&vendor=adoptium")
response = connection.getresponse()

body_data = response.read()

json_body = json.loads(body_data)

the_one = list(filter(lambda x: x["binary"]["os"] == "windows" and x["binary"]["architecture"] == "x64" and x["binary"]["image_type"] == "jdk", json_body))[0]

print(the_one["binary"]["package"]["link"])

connection.close()

if __name__ == "__main__":
    pass
