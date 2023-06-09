#! /usr/bin/env python3
import json

from opentelemetry import trace
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
from common import configure_tracer, log, Log
import requests
from opentelemetry.propagate import inject
from opentelemetry.trace import Status, StatusCode

tracer = configure_tracer("shop-service", "0.1.2")

@tracer.start_as_current_span("browse")
def browse():

    with tracer.start_as_current_span(
        "web request", kind=trace.SpanKind.CLIENT, record_exception=True
    ) as span:

        headers = {}
        inject(headers)
        url = "http://localhost:5000/products"
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
            if resp:
                data = json.loads(resp.content)
                add_item_to_cart(data)
                span.set_status(Status(StatusCode.OK))

            else:
                span.set_status(
                    Status(StatusCode.ERROR, "status code: {}".format(resp.status_code))
                )
            span.add_event("request sent", attributes={"url": url}, timestamp=0)
            span.set_attribute(
                SpanAttributes.HTTP_STATUS_CODE, resp.status_code
            )
        except Exception as err:
            span.record_exception(err)


@tracer.start_as_current_span("add item to cart")
def add_item_to_cart(data):

    with tracer.start_as_current_span("Adding item to cart", kind=trace.SpanKind.INTERNAL) as span:
        span.set_attributes(
            {
                "items": len(data)
            }
        )

    print("add {} to cart".format(data))


@tracer.start_as_current_span("visit store")
def visit_store():
    browse()


if __name__ == "__main__":
    visit_store()
