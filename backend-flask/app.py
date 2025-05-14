from flask import Flask

from lib.cognito_jwt_token import auth_checked
from lib.cors import configure_cors
from lib.rollbar import configure_rollbar

from routes.api import api as api_blueprint

# # aws x-ray
# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# # aws cloudwatch
# import watchtower
# import logging
# from time import strftime

app = Flask(__name__)

# Configure extensions and middleware
configure_cors(app)
configure_rollbar(app)

# # x-ray
# xray_url = os.getenv("AWS_XRAY_URL")
# xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
# XRayMiddleware(app, xray_recorder)

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

app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == "__main__":
  app.run(debug=True)