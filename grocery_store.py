import os

from flask import Flask, request
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
from opentelemetry.trace import SpanKind
from opentelemetry import context, trace
from opentelemetry.propagate import extract, inject, set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.trace.propagation import tracecontext
#from common import configure_tracer, set_span_attributes_from_flask
import requests

app = Flask(__name__)

# Using W3C and B3 propagators
set_global_textmap(CompositePropagator([tracecontext.TraceContextTextMapPropagator(), B3MultiFormat()]))

#tracer = configure_tracer("grocery-service", "0.1.2")


@app.route("/")
def welcome():
    return "Welcome to the grocery store !"


@app.route("/products")
def products():
    url = "{}".format(os.getenv("INVENTORY_URL"))
    resp = requests.get(url)
    return resp.text


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
