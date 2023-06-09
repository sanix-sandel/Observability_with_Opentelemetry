from flask import Flask, request
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
from opentelemetry.trace import SpanKind
from opentelemetry import context, trace
from opentelemetry.propagate import extract, inject, set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.trace.propagation import tracecontext
from common import configure_tracer, set_span_attributes_from_flask
import requests

app = Flask(__name__)

# Using W3C and B3 propagators
set_global_textmap(CompositePropagator([tracecontext.TraceContextTextMapPropagator(), B3MultiFormat()]))

tracer = configure_tracer("grocery-service", "0.1.2")


# We need to get the context before the decorator instantiates the span
@app.before_request
def before_request_func():
    token = context.attach(extract(request.headers))
    request.environ["context_token"] = token


@app.teardown_request
def teardown_request_func(err):
    token = request.environ.get("context_token", None)
    if token:
        context.detach(token)


@app.route("/")
@tracer.start_as_current_span("welcome", kind=SpanKind.SERVER)
def welcome():
    set_span_attributes_from_flask()
    return "Welcome to the grocery store !"


@app.route("/products")
@tracer.start_as_current_span("products", kind=SpanKind.SERVER)
def products():
    set_span_attributes_from_flask()
    with tracer.start_as_current_span("inventory request", kind=SpanKind.CLIENT) as span:
        trace_id = trace.get_current_span().get_span_context().trace_id
        url = "http://localhost:5001"
        span.set_attributes(
            {
                SpanAttributes.HTTP_METHOD: "GET",
                SpanAttributes.HTTP_FLAVOR: str(HttpFlavorValues.HTTP_1_1),
                SpanAttributes.HTTP_URL: url,
                SpanAttributes.NET_PEER_IP: "127.0.0.1",
            }
        )
        headers = {}
        inject(headers)
        resp = requests.get(url, headers=headers)
        return resp.text


if __name__ == "__main__":
    app.run(debug=True)
