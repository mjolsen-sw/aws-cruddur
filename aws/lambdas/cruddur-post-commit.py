import json
import os
import psycopg2

def lambda_handler(event, context):
  user = event['request']['userAttributes']
  try:
    conn = psycopg2.connect(
      host=(os.getenv('PG_HOSTNAME')),
      port=(os.getenv('PG_PORT')),
      database=(os.getenv('PG_DATABASE')),
      user=(os.getenv('PG_USERNAME')),
      password=(os.getenv('PG_SECRET'))
    )
    cur = conn.cursor()
    sql = """
            INSERT INTO users (display_name, handle, email, cognito_user_id)
            VALUES (%s, %s, %s, %s)
        """
    cur.execute(sql, (
      user.get('name'),
      user.get('preferred_username'),
      user.get('email'),
      user.get('sub')
    ))
    conn.commit()

  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
      
  finally:
    if conn in locals() and conn:
      cur.close()
      conn.close()
      print('Database connection closed.')

  return event