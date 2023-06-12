#! /usr/bin/env python3
import json

from flask import Flask, jsonify
from opentelemetry import trace
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
from common import configure_tracer, log, Log
import requests
from opentelemetry.propagate import inject
from opentelemetry.trace import Status, StatusCode

tracer = configure_tracer("shop-service", "0.1.2")

app = Flask(__name__)

@tracer.start_as_current_span("browse")
def browse():

    with tracer.start_as_current_span(
        "web request", kind=trace.SpanKind.CLIENT, record_exception=True
    ) as span:
        trace_id = trace.get_current_span().get_span_context().trace_id
        trace_id = '{:032x}'.format(trace_id)
        _log = Log(
            trace_id[:32],
            "",
            "shop-service"
        )
        log.info(_log)
        print(_log.trace_id)
        headers = {}
        inject(headers)
        url = "http://grocery-service:5000/products"
        span.set_attributes(
            {
                SpanAttributes.HTTP_METHOD: "GET",
                SpanAttributes.HTTP_FLAVOR: str(HttpFlavorValues.HTTP_1_1),
                SpanAttributes.HTTP_URL: url,
                SpanAttributes.NET_PEER_IP: "127.0.0.1"
            }
        )
        span.add_event("about to send a request")
        try:
            resp = requests.get(url, headers=headers)
            span.add_event("request sent", attributes={"url": url}, timestamp=0)

            if resp:
                data = json.loads(resp.content)
                span.set_status(Status(StatusCode.OK))
                span.set_attribute(
                    SpanAttributes.HTTP_STATUS_CODE, resp.status_code
                )
                return add_item_to_cart(data)

            else:
                span.set_status(
                    Status(StatusCode.ERROR, "status code: {}".format(resp.status_code))
                )

        except Exception as err:
            span.record_exception(err)


@tracer.start_as_current_span("add item to cart")
def add_item_to_cart(data):

    with tracer.start_as_current_span("Adding item to cart", kind=trace.SpanKind.INTERNAL) as span:
        trace_id = trace.get_current_span().get_span_context()
        span.set_attributes(
            {
                "items": len(data)
            }
        )
    print("add {} to cart".format(data))
    return jsonify(data)


@app.route("/")
@tracer.start_as_current_span("visit store")
def visit_store():
    return browse()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5555)
