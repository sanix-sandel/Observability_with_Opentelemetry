#! /usr/bin/env python3
import json
import os

from flask import Flask, jsonify
from opentelemetry import trace
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
# from common import configure_tracer, log, Log
import requests
from opentelemetry.propagate import inject
from opentelemetry.trace import Status, StatusCode


# tracer = configure_tracer("shop-service", "0.1.2")


app = Flask(__name__)


# @tracer.start_as_current_span("browse")
def browse():
    url = "{}/products".format(os.getenv("GROCERY_URL"))
    print("The url is {}".format(url))
    try:
        resp = requests.get(url)
        data = json.loads(resp.content)
        return add_item_to_cart(data)
    except Exception as err:
        print(err)


def add_item_to_cart(data):
    print("add {} to cart".format(data))
    return jsonify(data)


@app.route("/")
def visit_store():
    print("Visiting the grocery")
    return browse()


if __name__ == "__main__":
    print("Shopper started, The grocery url is {}".format(os.getenv("GROCERY_URL")))
    app.run(debug=True, host='0.0.0.0', port=5555)