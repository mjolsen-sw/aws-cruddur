import jwt
import os
from flask import request, jsonify
from functools import wraps

class FlaskAWSCognitoError(Exception):
    pass

class TokenVerifyError(Exception):
    pass

class CognitoJwtToken:
    def __init__(self, user_pool_id, user_pool_client_id, region):
        self.region = region
        if not self.region:
            raise FlaskAWSCognitoError("No AWS region provided")
        self.user_pool_id = user_pool_id
        self.user_pool_client_id = user_pool_client_id

    @staticmethod
    def _extract_headers(token):
        try:
            return jwt.get_unverified_header(token)
        except Exception as e:
            raise TokenVerifyError(str(e))

    def _get_public_key(self, kid):
        keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        jwks_client = jwt.PyJWKClient(keys_url)
        signing_key = jwks_client.get_signing_key(kid)
        return signing_key.key

    def _decode_token(self, token, public_key):
        try:
            return jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                issuer=f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}"
            )
        except jwt.ExpiredSignatureError:
            raise TokenVerifyError("Token has expired")
        except jwt.InvalidIssuerError as e:
            raise TokenVerifyError("Invalid Token Issuer")
        except Exception as e:
            raise FlaskAWSCognitoError(str(e))

    def verify(self, token):
        if not token:
            raise TokenVerifyError("No token provided")
        headers = self._extract_headers(token)
        public_key = self._get_public_key(headers["kid"])
        user_info = self._decode_token(token, public_key)
        return user_info

cognito_jwt_token = CognitoJwtToken(
  user_pool_id=os.getenv('AWS_COGNITO_USER_POOL_ID'),
  user_pool_client_id=os.getenv('AWS_COGNITO_USER_POOL_CLIENT_ID'),
  region=os.getenv('AWS_DEFAULT_REGION')
)

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