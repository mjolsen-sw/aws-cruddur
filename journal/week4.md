# Week 4 — Postgres and RDS
## PSQL
### Log into containerized database
```sh
psql -U postgres --host localhost
```
### Common PSQL commands
```sh
\x on -- expanded display when looking at data
\q -- Quit PSQL
\l -- List all databases
\c database_name -- Connect to a specific database
\dt -- List all tables in the current database
\d table_name -- Describe a specific table
\du -- List all users and their roles
\dn -- List all schemas in the current database
CREATE DATABASE database_name; -- Create a new database
DROP DATABASE database_name; -- Delete a database
CREATE TABLE table_name (column1 datatype1, column2 datatype2, ...); -- Create a new table
DROP TABLE table_name; -- Delete a table
SELECT column1, column2, ... FROM table_name WHERE condition; -- Select data from a table
INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...); -- Insert data into a table
UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition; -- Update data in a table
DELETE FROM table_name WHERE condition; -- Delete data from a table
```
### Create the database
```sh
createdb cruddur -h localhost -U postgres
```
```sh
CREATE DATABASE cruddur;
```
```sh
DROP DATABASE cruddur;
```
### Import Script
We'll create a new SQL file called schema.sql and we'll place it in `backend-flask/db`
```sh
psql -h localhost -p 2345 -U postgres -d cruddur < db/schema.sql
```
Using Windows Command Prompt (cmd):\
```sh
psql -h localhost -U postgres -d cruddur < db/schema.sql
```
### Add UUID Extension
We are going to have Postgres generate out UUIDs so we'll need to use an extention:
```sh
CREATE EXTENSION "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```
### Connection String
```sh
export CONNECTION_URL="postgresql://postgres:password@localhost:2345/cruddur"
```
### Create our table
Add table creation to 'schema.sql':
```sh
CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text,
  handle text
  cognito_user_id text,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```
```sh
CREATE TABLE public.activities (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  reply_to_activity_uuid integer,
  expires_at TIMESTAMP,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```
```sh
CREATE TABLE public.reply (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  reply_to_activity_uuid UUID,
  display_name text,
  handle text,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```
```sh
CREATE TABLE public.message (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text,
  handle text,
  message text NOT NULL,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```
```sh
CREATE TABLE public.message_group (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text,
  handle text
);
```
```sh
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;
DROP TABLE IF EXISTS public.reply;
DROP TABLE IF EXISTS public.message;
DROP TABLE IF EXISTS public.message_group;
```
### psycogp DB connection string with WSL
To allow psycogp to connect to Docker container in WSL, use hostname **host.docker.internal**:
```sh
export PP_CONNECTION_URL="postgresql://username:password@host.docker.internal:2345/cruddur";
```
### Lambda to insert new users into DB
#### Create Labmda
ENV variables used (best practice would be parameter store or secrets manager):
```sh
PG_HOSTNAME='db.endpoint.url'
PG_DATABASE='cruddur'
PG_USERNAME='cruddur'
PG_PASSWORD='password'
```
The function:
```python
import json
import psycopg2

def lambda_handler(event, context):
  user = event['request']['userAttributes']
  print("user:", user)
  try:
    conn = psycopg2.connect(
      host=(os.getenv('PG_HOSTNAME')),
      database=(os.getenv('PG_DATABASE')),
      user=(os.getenv('PG_USERNAME')),
      password=(os.getenv('PG_SECRET'))
    )
    cur = conn.cursor()
    sql = f"""
      INSERT INTO users (
        display_name,
        handle,
        email,
        cognito_user_id
        )
      VALUES(
        {user['name']},
        {user['preferred_username']},
        {user['sub']}
        )
    """
    cur.execute(sql)
    conn.commit() 

  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
      
  finally:
    if conn is not None:
      cur.close()
      conn.close()
      print('Database connection closed.')

  return event
```
##### Creating psycopg2 Lambda Layer
###### Create new directory for the layer in `aws/lambdas/`
```sh
mkdir -p psycopg2-layer/python
cd psycopg2-layer/python
```
###### Install psycopg-binary with python version used (ex. 3.10 on x86_64)
```sh
pip3 install --platform manylinux2014_x86_64 --target . --python-version 3.10 --only-binary=:all: psycopg2-binary
```
###### Package the Layer
Zip the contents of the python directory:
```sh
cd ..
zip -r psycopg2-layer.zip python
```
###### Upload to AWS Lambda