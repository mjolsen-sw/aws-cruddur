import jwt

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
            return {"error": "Token has expired"}
        except jwt.InvalidIssuerError as e:
            raise {"error": "Invalid Token Issuer"}
        except Exception as e:
            raise FlaskAWSCognitoError(str(e))

    def verify(self, token):
        if not token:
            raise TokenVerifyError("No token provided")
        headers = self._extract_headers(token)
        public_key = self._get_public_key(headers["kid"])
        user_info = self._decode_token(token, public_key)
        return user_info