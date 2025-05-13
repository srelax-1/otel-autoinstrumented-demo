FROM docker.io/python:3-slim

WORKDIR /app

COPY ./student_app /app

# Install requirement.txt and Opentementry package
RUN pip install -r requirements.txt && \
    pip install opentelemetry-distro opentelemetry-exporter-otlp && \
    opentelemetry-bootstrap --action=install

# Make port 5000 available to the world outside this container
EXPOSE 5000

# ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4317"
# # ENV OTEL_EXPORTER_OTLP_PROTOCOL: http/protobuf
# ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc
# ENV OTEL_METRICS_EXPORTER="otlp"
# ENV OTEL_TRACES_EXPORTER="otlp"
# ENV OTEL_LOGS_EXPORTER="otlp"
# ENV OTEL_SERVICE_NAME=student
# ENV OTEL_LOG_LEVEL=debug
# ENV OTEL_RESOURCE_ATTRIBUTES="deployment.environment=dev,service.namespace=school-api"


# CMD ["flask", "run", "-p", "5000"]
CMD ["opentelemetry-instrument", "python","student.py"]