import os
import sys
import time

import requests

API = "https://graph.facebook.com/v26.0"
TOKEN = os.environ["IG_ACCESS_TOKEN"]
IG_USER_ID = os.environ["IG_USER_ID"]

image_url = sys.argv[1]
caption = sys.argv[2] if len(sys.argv) > 2 else ""


def call(method, path, **params):
    r = requests.request(
        method,
        f"{API}/{path}",
        params=params,
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=30,
    )
    if not r.ok:
        sys.exit(f"instagram api error {r.status_code}: {r.text}")
    return r.json()



for _ in range(15):
    if requests.head(image_url, timeout=10, allow_redirects=True).status_code == 200:
        break
    time.sleep(2)
else:
    sys.exit(f"image url aint reachable bro... {image_url}")

container_id = call("POST", f"{IG_USER_ID}/media", image_url=image_url, caption=caption)["id"]
print("container:", container_id)


for _ in range(20):
    status = call("GET", container_id, fields="status_code")["status_code"]
    if status == "FINISHED":
        break
    if status in ("ERROR", "EXPIRED"):
        sys.exit(f"container status: {status}")
    time.sleep(3)
else:
    sys.exit("timed out waiting for container to finish")

post_id = call("POST", f"{IG_USER_ID}/media_publish", creation_id=container_id)["id"]
print("published:", post_id)
