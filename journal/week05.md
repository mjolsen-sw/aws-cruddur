# Week 5 — DynamoDB and Serverless Caching
## DynamoDB Python and Bash Scripts
```sh
./backend-flask/bin/ddb/*
```
## The Boundaries of DynamoDB
- When you write a query you have provide a Primary Key (equality) eg. pk = 'GRP#1e057ec3-a40a-4133-b170-92f56a762c45'
- Are you allowed to "update" the Hash and Range?
  - No, whenever you change a key (simple or composite) eg. pk or sk you have to create a new item.
    - you have to delete the old one
- Key condition expressions for query only for RANGE, HASH is only equality 
- Don't create UUID for entity if you don't have an access pattern for it
## Access Patterns
### Pattern A  (showing a single conversation)
A user wants to see a list of messages that belong to a message group
The messages must be ordered by the created_at timestamp from newest to oldest (DESC)
```sql
SELECT
  messages.pk,
  messages.display_name,
  messages.message,
  messages.handle,
  messages.created_at -- sk
FROM messages
WHERE
  messages.message_group_uuid  = {{message_group_uuid}} -- pk
ORDER BY messages.created_at DESC -- sk
```
> message_group_uuid comes from Pattern B
### Pattern B (list of conversations)
A user wants to see a list of previous conversations.
These conversations are listed from newest to oldest (DESC)
We want to see the other person we are talking to.
We want to see the last message (from whomever) in summary.
```sql
SELECT
  message_groups.uuid,
  message_groups.other_user_uuid,
  message_groups.other_user_display_name,
  message_groups.other_user_handle,
  message_groups.last_message,
  message_groups.last_message_at
FROM message_groups
WHERE
  message_groups.user_uuid = {{user_uuid}} --pk
ORDER BY message_groups.last_message_at DESC
```
> We need a Global Secondary Index (GSI)
### Pattern C (create a message)
```sql
INSERT INTO messages (
  user_uuid,
  display_name,
  handle,
  created_at
)
VALUES (
  {{user_uuid}},
  {{display_name}},
  {{handle}},
  {{created_at}}
);
```
### Pattern D (update a message_group for the last message)
When a user creates a message we need to update the conversation
to display the last message information for the conversation. Keep
in mind this requires deleting and recreating instead of updating.
```sql
UPDATE message_groups
SET 
  other_user_uuid = {{other_user_uuid}}
  other_user_display_name = {{other_user_display_name}}
  other_user_handle = {{other_user_handle}}
  last_message = {{last_message}}
  last_message_at = {{last_message_at}}
WHERE 
  message_groups.uuid = {{message_group_uuid}}
  AND message_groups.user_uuid = {{user_uuid}}
```
## DynamoDB Stream trigger to update message groups
### Create production table and enable stream
1. Create production table:
'''sh
./backend-flash/bin/ddb/schema-load prod
'''
2. Open `cruddur-messages` DynamoDB table in AWS console
3. Navigate to `Exports and streams` tab
4. Under `DynamoDB stream details`, click **Turn on**
5. Select `New image` and click **Turn on stream**
### Create VPC endpoint for DynamoDB service in the VPC
1. Go to `VPC` service and select `Endpoints` on the sidebar
2. Click **Create endpoint** button on the upper right
3. Name the endpoint under `Endpoint settings` (eg. cruddur-ddb-endpoint)
4. Under `Services`, filter for **dynamodb** and select the `Gateway` **Type**
5. Select the cruddur VPC under `Network settings`
6. Select the route table under `Route tables`
7. Leave the `Policy` section as is
8. Click **Create endpoint** at bottom right
### Create Python lambda function in the VPC
#### Create Lambda
1. Name function (eg. cruddur-messaging-stream) and select `Runtime` (eg. Python 3.10)
2. Select `Change default execution role`
3. Select `Create a new role with basic Lambda permissions` (this will be changed later)
4. Under `Additional Configurations` select `Enable VPC` and select the VPC
5. Under `Subnets` select your subnets
6. Use the default security group
7. Click **Create function** at the bottom right
#### The Function
Use the code from `./aws/lambdas/cruddur-messaging-stream.py`
#### Update Role
1. Select the `Configuration` tab
2. Select `Permissions` on the sidebar
3. Select the role under `Role name` to go to `IAM > Roles` (eg. 
cruddur-messaging-stream-role-kplzdgtb)
4. Attach an inline policy in the file `./aws/policies/cruddur-message-stream-policy.json`
5. Attach `AWSLambdaInvocation-DynamoDB`
#### Add function to be triggered by DynamoDB Stream
1. Go to your DynamboDB table (eg. `DynamoDB > Tables > cruddur-messages`)
2. Scroll down to `Trigger` and click **Create trigger**
3. Select your function and create
