import json
import requests
import os

if __name__=="__main__":
    print("Job will start checking inventory")
    url = "{}".format(os.getenv("INVENTORY_URL"))
    resp = requests.get(url)
    print(json.loads(resp.content))
    print("Job finished its treatment")
