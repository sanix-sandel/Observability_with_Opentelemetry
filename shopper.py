#! /usr/bin/env python3
from opentelemetry import trace
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
from common import tracer
import requests
from opentelemetry.propagate import inject


@tracer.start_as_current_span("browse")
def browse():
    print("Visiting the grocery store")
    with tracer.start_as_current_span(
        "web request", kind=trace.SpanKind.CLIENT
    ) as span:
        headers = {}
        inject(headers)
        url = "http://localhost:5000"
        span.set_attributes(
            {
                SpanAttributes.HTTP_METHOD: "GET",
                SpanAttributes.HTTP_FLAVOR: str(HttpFlavorValues.HTTP_1_1),
                SpanAttributes.HTTP_URL: url,
                SpanAttributes.NET_PEER_IP: "127.0.0.1"
            }
        )

        resp = requests.get(url, headers=headers)
        span.set_attribute(
            SpanAttributes.HTTP_STATUS_CODE, resp.status_code
        )


@tracer.start_as_current_span("add item to cart")
def add_item_to_cart(item, quantity):
    span = trace.get_current_span()
    span.set_attributes(
        {
            "item": item,
            "quantity": quantity
        }
    )
    print("add {} to cart".format(item))


@tracer.start_as_current_span("visit store")
def visit_store():
    browse()


if __name__ == "__main__":
    visit_store()
