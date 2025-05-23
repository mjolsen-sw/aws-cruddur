import atexit
import os
import re
import sys
from flask import current_app as app
from psycopg_pool import ConnectionPool

class Db:
  def __init__(self):
    self._init_pool()
    atexit.register(self._close_pool)
  
  def _init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self._pool = ConnectionPool(connection_url)
    
  def _close_pool(self):
    if self._pool:
      self._pool.close()

  @staticmethod
  def template(*args):
    pathing = list((app.root_path, "db", "sql",) + args)
    pathing[-1] = pathing[-1] + ".sql"

    template_path = os.path.join(*pathing)

    print("\n")
    print(f" Load SQL Template: {template_path}")

    with open(template_path, "r") as f:
      template_content = f.read()
    return template_content

  @staticmethod
  def print_params(params):
    print(" SQL Params:")
    for key, value in params.items():
      print(key, ":", value)
  
  @staticmethod
  def print_sql(title, sql):
    print(f" SQL STATEMENT-[{title}]------")
    print(sql)
  
  @staticmethod
  def print_sql_err(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg ERROR:", err, "on line number:", line_num)
    print ("psycopg traceback:", traceback, "-- type:", err_type)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")

  @staticmethod
  def query_wrap_object(template):
    sql = f"""
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    """
    return sql

  @staticmethod
  def query_wrap_array(template):
    sql = f"""
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    """
    return sql

  # we want to commit data such as an insert
  # be sure to check for RETURNING in all uppercases
  def query_commit(self, sql, params=None, verbose=True):
    if params is None:
      params = {}
    
    if verbose:
      self.print_sql('commit with returning', sql)
      self.print_params(params)

    pattern = r"\bRETURNING\b"
    is_returning_id = re.search(pattern, sql)

    try:
      with self._pool.connection() as conn:
        cur =  conn.cursor()
        cur.execute(sql, params)
        if is_returning_id:
          returning_id = cur.fetchone()[0]
        conn.commit() 
        if is_returning_id:
          return returning_id
    except Exception as err:
      self.print_sql_err(err)

  # when we want to return an array json objects
  def query_array_json(self, sql, params=None, verbose=True):
    if params is None:
      params = {}
    
    if verbose:
      self.print_sql('array', sql)
      self.print_params(params)

    wrapped_sql = self.query_wrap_array(sql)
    with self._pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql, params)
        json = cur.fetchone()
        return json[0]

  # When we want to return a json object
  def query_object_json(self, sql, params=None, verbose=True):
    if params is None:
      params = {}
    
    if verbose:
      self.print_sql('json', sql)
      self.print_params(params)

    wrapped_sql = self.query_wrap_object(sql)
    with self._pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql, params)
        json = cur.fetchone()
        if json == None:
          return "{}"
        else:
          return json[0]
  
  def query_value(self, sql, params=None, verbose=True):
    if params == None:
      params = {}
    
    if verbose:
      self.print_sql('value', sql)
      self.print_params(params)

    with self._pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql, params)
        json = cur.fetchone()
        return json[0]

db = Db()