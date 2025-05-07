import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource(
 'dynamodb',
 region_name='us-west-1',
 endpoint_url='http://dynamodb.us-west-1.amazonaws.com'
)

# Read environment variables
TABLE_NAME = os.environ['TABLE_NAME']   # e.g. cruddur-messages
INDEX_NAME = os.environ['INDEX_NAME']   # e.g. message-group-sk-index

def lambda_handler(event, context):
  eventName = event['Records'][0]['eventName']
  if (eventName == 'REMOVE'):
    print("skip REMOVE event")
    return

  pk = event['Records'][0]['dynamodb']['Keys']['pk']['S']
  sk = event['Records'][0]['dynamodb']['Keys']['sk']['S']
  if pk.startswith('MSG#'):
    group_uuid = pk.replace("MSG#", "")
    message = event['Records'][0]['dynamodb']['NewImage']['message']['S']
    print("GROUP ===>", group_uuid, message)
    
    table = dynamodb.Table(TABLE_NAME)
    data = table.query(
      IndexName=INDEX_NAME,
      KeyConditionExpression=Key('message_group_uuid').eq(group_uuid)
    )
    print("RESP ===>", data['Items'])
    
    # recreate the message group rows with new SK value
    for i in data['Items']:
      delete_item = table.delete_item(Key={'pk': i['pk'], 'sk': i['sk']})
      print("DELETE ===>", delete_item)
      
      response = table.put_item(
        Item={
          'pk': i['pk'],
          'sk': sk,
          'message_group_uuid': i['message_group_uuid'],
          'message': message,
          'user_display_name': i['user_display_name'],
          'user_handle': i['user_handle'],
          'user_uuid': i['user_uuid']
        }
      )
      print("CREATE ===>", response)