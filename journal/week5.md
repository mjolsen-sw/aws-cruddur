# Week 5 — DynamoDB and Serverless Caching
## DynamoDB Python and Bash Scripts
```sh
./bin/ddb/schem-load
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
  messages.pk = "MSG#{{message_group_uuid}}" -- pk
ORDER BY messages.created_at DESC
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
  message_groups.pk = "GRP#{{user_uuid}}" --pk
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
to display the last message information for the conversation
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
