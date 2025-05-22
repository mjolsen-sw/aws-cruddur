import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

def configure_rollbar(app):
  """Initialize Rollbar exception tracking for the Flask app."""
  rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
  flask_env = os.getenv('FLASK_ENV')
  rollbar.init(
    # access token
    rollbar_access_token,
    # environment name
    flask_env,
    # server root directory, makes tracebacks prettier
    root=os.path.dirname(os.path.realpath(__file__)),
    # flask already sets up logging
    allow_logging_basic_config=False
  )
  # send exceptions from `app` to rollbar, using flask's signal system.
  got_request_exception.connect(rollbar.contrib.flask.report_exception, app)