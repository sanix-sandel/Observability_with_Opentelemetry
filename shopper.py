#! /usr/bin/env python3
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from local_machine_resource_detector import LocalMachineResourceDetector


def configure_tracer(name, version):
    exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(exporter)
    local_resource = LocalMachineResourceDetector().detect()
    resource = local_resource.merge(
        Resource.create(
            {
                "service.name": name,
                "service.version": version
            }
        )
    )
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer(name, version)


tracer = configure_tracer("shopper", "0.1.2")


@tracer.start_as_current_span("browse")
def browse():
    print("Visiting the grocery store")
    add_item_to_cart("Orange")
    span = trace.get_current_span()
    span.set_attribute("http.method", "GET")
    span.set_attribute("http.flavor", "1.1")
    span.set_attribute("http.url", "http://localhst:5000")
    span.set_attribute("net.peer.ip", "127.0.0.1")


@tracer.start_as_current_span("add item to cart")
def add_item_to_cart(item):
    print("add {} to cart".format(item))


@tracer.start_as_current_span("visit store")
def visit_store():
    browse()


if __name__ == "__main__":
    visit_store()
