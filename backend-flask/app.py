from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from functools import wraps
import os

# honeycomb.io
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

from lib.cognito_jwt_token import *
from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.users_short import *
from services.update_profile import *

# # aws x-ray
# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# # aws cloudwatch
# import watchtower
# import logging
# from time import strftime

# honeycomb.io
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(simple_processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)

# AWS Cognito
cognito_jwt_token = CognitoJwtToken(
  user_pool_id=os.getenv('AWS_COGNITO_USER_POOL_ID'),
  user_pool_client_id=os.getenv('AWS_COGNITO_USER_POOL_CLIENT_ID'),
  region=os.getenv('AWS_DEFAULT_REGION')
)

# honeycomb.io
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# # x-ray
# xray_url = os.getenv("AWS_XRAY_URL")
# xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
# XRayMiddleware(app, xray_recorder)

import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  supports_credentials=True,
  allow_headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)

rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
@app.before_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

# # Configuring Logger to Use CloudWatch
# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
# LOGGER.addHandler(console_handler)
# LOGGER.addHandler(cw_handler)

# @app.after_request
# def after_request(response):
#     timestamp = strftime('[%Y-%b-%d %H:%M]')
#     LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
#     return response

def auth_checked(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      request.cognito_user_id = None
      auth_header = request.headers.get("Authorization")

      if auth_header:
        try:
          token = auth_header.split(" ")[1]  # Remove "Bearer " prefix
          user_info = cognito_jwt_token.verify(token)
          request.cognito_user_id = user_info["username"]
        except TokenVerifyError as e:
          print(f"TokenVerifyError: {e}")
        except FlaskAWSCognitoError as e:
          print(f"FlaskAWSCognitoError: {e}")
        except Exception as e:
          print(f"Unexcepted exception: {e}")

      else:
        print("Missing token")

      return f(*args, **kwargs)

    return decorated_function

@app.route('/api/health-check')
def health_check():
  return {'success': True}, 200

@app.route("/api/message_groups", methods=['GET'])
@auth_checked
def data_message_groups():
  cognito_user_id = request.cognito_user_id
  if cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  model = MessageGroups.run(cognito_user_id=cognito_user_id)
  if len(model['errors']) > 0:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/messages/<string:message_group_id>", methods=['GET'])
@auth_checked
def data_messages(message_group_id):
  model = Messages.run(
    cognito_user_id=request.cognito_user_id,
    message_group_id=message_group_id
  )

  if len(model['errors']) > 0:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
@auth_checked
def data_create_message():
  cognito_user_id = request.cognito_user_id
  if cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401

  message = request.json['message']
  user_receiver_handle = request.json.get('handle', None)
  message_group_uuid = request.json.get('message_group_uuid', None)

  mode = 'create' if message_group_uuid == None else 'update'

  model = CreateMessage.run(
    mode=mode,
    cognito_user_id=cognito_user_id,
    message_group_uuid=message_group_uuid,
    message=message,
    user_receiver_handle=user_receiver_handle
  )
  
  if len(model['errors']) > 0:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/profile/update", methods=['POST','OPTIONS'])
@cross_origin()
@auth_checked
def data_update_profile():
  cognito_user_id = request.cognito_user_id
  print('cognito_user_id:', cognito_user_id)
  if cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401

  bio          = request.json.get('bio',None)
  display_name = request.json.get('display_name',None)
  
  model = UpdateProfile.run(
    cognito_user_id=cognito_user_id,
    bio=bio,
    display_name=display_name
  )
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/users/@<string:handle>/short")
def data_short(handle):
  data = UsersShort.run(handle)
  return data, 200

@app.route("/api/activities/home", methods=['GET'])
@auth_checked
def data_home():
  data = HomeActivities.run(request.cognito_user_id)
  return data, 200

@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
@auth_checked
def data_handle(handle):
  if request.cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  model = UserActivities.run(handle)
  if len(model['errors']) > 0:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
@auth_checked
def data_activities():
  cognito_user_id = request.cognito_user_id
  if cognito_user_id is None:
    return { 'error': 'Not logged in' }, 401
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, cognito_user_id, ttl)
  if len(model['errors']) > 0:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

if __name__ == "__main__":
  app.run(debug=True)