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
      OTEL_SERVICE_NAME: "backend-flask"
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

## AWS X-Ray
### Instrument AWS X-Ray for Flask
Set region environment variable.
Linux:
```sh
export AWS_REGION="us-west-1"
```
Windows:
```sh
[Environment]::SetEnvironmentVariable("AWS_REGION", "us-west-1", "User")
```
Add dependency to `requirements.txt` and install:
```sh
aws-xray-sdk
```
```sh
pip install -r requirements.txt
```
Add to app.y
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='Cruddur', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)
```

### Setup AWS X-Ray Resources
Use `aws/json/xray.json` to setup.
Linux:
```sh
FLASK_ADDRESS="http://127.0.0.1:4567"
aws xray create-group \
   --group-name "Cruddur" \
   --filter-expression "service(\"$FLASK_ADDRESS\") {fault OR error}"
```
Windows Powershell:
```sh
$env:FLASK_ADDRESS = "http://127.0.0.1:4567"
aws xray create-group --group-name "Cruddur" --filter-expression 'service(\"backend-flask\")'
```
Then create the sampling rule:
```sh
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
```

### Add Daemon Service to Docker Compose
```yml
  xray-daemon:
    image: "amazon/aws-xray-daemon"
    environment:
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      AWS_REGION: "us-west-1"
    command:
      - "xray -o -b xray-daemon:2000"
    ports:
      - 2000:2000/udp
```
Also add two environment variables for our backend container:
```yml
      AWS_XRAY_URL: "127.0.0.1:4567"
      AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"
```

## CloudWatch Log
Add to `requirements.txt` and install.
```sh
watchtower
```
Add to app.py:
```python
import watchtower
import logging
from time import strftime
```
```python
# Configuring Logger to Use CloudWatch
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("some message")
```
```python
@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response
```
You can log something to an API endpoint. Example:
```python
LOGGER.info('Hello Cloudwatch! from  /api/activities/home')
```
Add 3 more environment variables for backend-flask in `docker-compose.yml`.
(boto3 doesn't get AWS_REGION so pass default region instead):
```yml
      AWS_DEFAULT_REGION: "${AWS_DEFAULT_REGION}"
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
```

