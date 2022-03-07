import argparse
import json
import platform
import ssl

import http.client
import urllib.parse
import urllib.request


def get_jdk_list(
    jdk_version: str,
    release: str = "release",
    jvm_impl: str = "jvm_impl",
    vendor: str = "vendor"
) -> list[dict]:
    connection = http.client.HTTPSConnection(
        "api.adoptium.net", context=ssl._create_unverified_context())

    connection.request(
        method="GET",
        url="/v3/assets/latest/{}/hotspot?{}".format(jdk_version, urllib.parse.urlencode({"release": "latest", "jvm_impl": "hotspot", "vendor": "adoptium"}))
    )
    response = connection.getresponse()

    data = json.loads(response.read())

    connection.close()

    return data


os_mapping = {
    "Linux": "linux",
    "Darwin": "mac",
    "Windows": "windows"
}

if __name__ == "__main__":
    system: str = platform.system()
    
    jdk_list: list[dict] = get_jdk_list("11")

    jdk_select_one = list(filter(lambda e: e["binary"]["os"] == os_mapping[system] and e["binary"]["image_type"] == "jdk" and e["binary"]["architecture"] == "x64", jdk_list))

    assert len(jdk_select_one) == 1

    jdk = jdk_select_one[0]

    download_link = jdk["binary"]["package"]["link"]

    proxy = urllib.request.ProxyHandler({'https': 'http://localhost:1091'})
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)

    code, msg = urllib.request.urlretrieve(download_link, "jdk.zip")
    print(code, msg)
