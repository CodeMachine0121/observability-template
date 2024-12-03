from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs.export import ConsoleLogExporter, BatchLogRecordProcessor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
import logging
import time

# 設定 Resource
resource = Resource.create({
    "service.name": "python-test-service",
    "service.version": "1.0.0"
})

# 設定 Logs
logger_provider = LoggerProvider(resource=resource)
otlp_log_exporter = OTLPLogExporter(endpoint="http://localhost:14317")
logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

# 設定 Python logger
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# 產生一些測試日誌
for i in range(5):
    logger.info(f"Test log message {i}", extra={
        "custom_field": f"value_{i}",
        "test_number": i
    })
    time.sleep(1)

    try:
        if i == 3:
            raise Exception("Test error")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", extra={
            "error_count": i,
            "error_type": "test_error"
        })

time.sleep(5)  # 等待日誌被發送
