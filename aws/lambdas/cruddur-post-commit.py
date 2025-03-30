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