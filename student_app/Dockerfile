FROM docker.io/python:3-slim

WORKDIR /app

COPY ./ ./

# Install requirement.txt and Opentementry package
RUN pip install -r requirements.txt && \
    pip install opentelemetry-distro opentelemetry-exporter-otlp opentelemetry-instrumentation-flask opentelemetry-sdk opentelemetry-exporter-prometheus && \
    pip install opentelemetry-instrumentation-wsgi opentelemetry-instrumentation && \
    opentelemetry-bootstrap --action=install

# Make port 5000 available to the world outside this container
EXPOSE 5000

# CMD ["flask", "run", "-p", "5000"]
CMD ["opentelemetry-instrument", "python","student.py"]