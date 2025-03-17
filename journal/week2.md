# Week 2 — Distributed Tracing
## HoneyComb
### Set Environment Variables
For Linux:
```sh
export HONEYCOMB_API_KEY="<api_key>"
export HONEYCOMB_SERVICE_NAME="Cruddur"
```
For Windows Powershell temporary:
```sh
$env:HONEYCOMB_API_KEY = "<api_key>"
$env:HONEYCOMB_SERVICE_NAME = "Cruddur"
```
For Windows Powershell permanent:
```sh
[Environment]::SetEnvironmentVariable("HONEYCOMB_API_KEY", "<api_key>", "User")
[Environment]::SetEnvironmentVariable("HONEYCOMB_SERVICE_NAME", "Cruddur", "User")
```

### Add Environmental Variable to docker-compose.yml
Under backend-flask's environment:
```yml
      OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
      OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
      OTL_SERVICE_NAME: "backend-flask"
```

### Add to app.py
Add libraries to requirements.txt:
```sh
opentelemetry-api 
opentelemetry-sdk 
opentelemetry-exporter-otlp-proto-http 
opentelemetry-instrumentation-flask 
opentelemetry-instrumentation-requests
```
Add the following code to app.py:
```python
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
```

### Tracing in python code
Add at the top of the file:
```python
from opentelemetry import trace

tracer = trace.get_tracer("unique.identifier")
```
In the method of the code that's run, you can add attributes to logging messages.
Example of adding the timestamp to the log:
```python
def run():
    with tracer.start_as_current_span("unique-identifier-action-identifier"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())
```