import boto3
import json
import os
import psycopg2
import requests
from jose import jwt, JWTError

s3_client = boto3.client('s3')
ssm_client = boto3.client('ssm')

# Required environment variables
BUCKET_NAME = os.environ['UPLOADS_BUCKET_NAME']
COGNITO_USERPOOL_ID = os.environ['AWS_COGNITO_USER_POOL_ID']
COGNITO_REGION = os.environ['AWS_REGION']
SSM_CONN_PARAM = "/cruddur/backend-flask/CONNECTION_URL"

# JWKS URL
JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USERPOOL_ID}/.well-known/jwks.json"

# Cache JWKS
_jwks = None
_connection_url = None

def get_jwks():
  global _jwks
  if _jwks is None:
    _jwks = requests.get(JWKS_URL).json()
  return _jwks

def get_connection_url():
    global _connection_url
    if _connection_url is None:
        response = ssm_client.get_parameter(Name=SSM_CONN_PARAM, WithDecryption=True)
        _connection_url = response['Parameter']['Value']
    return _connection_url

def get_user_handle(cognito_sub):
  conn_url = get_connection_url()
  conn = psycopg2.connect(conn_url)
  try:
    with conn.cursor() as cursor:
      cursor.execute(
        "SELECT handle FROM users WHERE cognito_user_id = %s",
        (cognito_sub,)
      )
      result = cursor.fetchone()
      if result:
        return result[0]
      else:
        raise ValueError("User not found in database")
  finally:
    conn.close()

def lambda_handler(event, context):
  try:
    # Extract the token from the Authorization header
    auth_header = event['headers'].get('Authorization', '')
    if not auth_header.startswith('Bearer '):
      return {
        "statusCode": 401,
        "body": json.dumps({"error": "Missing or invalid Authorization header"})
      }

    token = auth_header.split(' ')[1]

    # Decode and verify the token
    jwks = get_jwks()
    claims = jwt.decode(token, jwks, algorithms=['RS256'], audience=None, issuer=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USERPOOL_ID}")

    user_id = claims.get('sub')
    if not user_id:
      raise ValueError("Invalid token: no 'sub' claim found")
    
    # Fetch handle from DB
    handle = get_user_handle(user_id)

    # Generate the S3 key
    file_extension = 'jpg'
    content_type = 'image/jpeg'
    filename = f"{handle}.{file_extension}"

    presigned_url = s3_client.generate_presigned_url(
      'put_object',
      Params={
        'Bucket': BUCKET_NAME,
        'Key': filename,
        'ContentType': content_type
      },
      ExpiresIn=300
    )

    return {
      "statusCode": 200,
      "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      "body": json.dumps({
        "upload_url": presigned_url,
        "file_key": filename
      })
    }
  except JWTError as e:
    print(f"JWT decode error: {e}")
    return {
      "statusCode": 401,
      "body": json.dumps({"error": "Invalid token"})
    }
  except Exception as e:
    print(f"Error generating presigned URL: {e}")
    return {
      "statusCode": 500,
      "body": json.dumps({"error": "Failed to generate presigned URL"})
    }