# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
# from opentelemetry.sdk.resources import Resource
# from local_machine_resource_detector import LocalMachineResourceDetector
# from opentelemetry.semconv.resource import ResourceAttributes
# from opentelemetry.semconv.trace import SpanAttributes
# from opentelemetry.exporter.jaeger.thrift import JaegerExporter
# import logging
# from flask import request
#
#
# jaeger_exporter = JaegerExporter(
#     agent_host_name='127.0.0.1',
#     agent_port=6831
# )
#
#
# log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
# log_handler = logging.StreamHandler()
# log_handler.setLevel(logging.INFO)
# log_handler.setFormatter(log_formatter)
#
#
# log = logging.getLogger("MyLogger")
# log.addHandler(log_handler)
#
#
# class Log:
#     def __init__(self, trace_id, msg, service):
#         self.trace_id = trace_id
#         self.msg = msg
#         self.service = service
#
#
# def set_span_attributes_from_flask():
#     span = trace.get_current_span()
#     span.set_attributes(
#         {
#             SpanAttributes.HTTP_FLAVOR: request.environ.
#             get("SERVER_PROTOCOL"),
#             SpanAttributes.HTTP_METHOD: request.method,
#             SpanAttributes.HTTP_USER_AGENT: str(request.user_agent),
#             SpanAttributes.HTTP_HOST: request.host,
#             SpanAttributes.HTTP_SCHEME: request.scheme,
#             SpanAttributes.HTTP_TARGET: request.path,
#             SpanAttributes.HTTP_CLIENT_IP: request.remote_addr,
#         }
#     )
#
#
# def configure_tracer(name, version):
#     exporter = jaeger_exporter
#     span_processor = BatchSpanProcessor(exporter)
#     local_resource = LocalMachineResourceDetector().detect()
#     resource = local_resource.merge(
#         Resource.create(
#             {
#                 ResourceAttributes.SERVICE_NAME: name,
#                 ResourceAttributes.SERVICE_VERSION: version
#             }
#         )
#     )
#     provider = TracerProvider(resource=resource)
#     provider.add_span_processor(span_processor)
#     trace.set_tracer_provider(provider)
#
#     return trace.get_tracer(name, version)
