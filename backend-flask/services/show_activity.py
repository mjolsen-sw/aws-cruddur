from aws_xray_sdk.core import xray_recorder

from lib.db import db

class ShowActivity:
  @staticmethod
  def run(activity_uuid):
    with xray_recorder.in_segment('show_activity_run') as segment:
      model = {
        'errors': [],
        'data': None
      }

      if activity_uuid == None or len(activity_uuid) < 1:
        model['errors'] += ['activity_uuid_blank'] 
      elif len(activity_uuid) > 36:
        model['errors'] += ['activity_uuid_exceed_max_chars']

      segment.put_annotation("show.activity.uuid", activity_uuid)
      if len(model['errors']) == 0:
        data = ShowActivity.show_activity_info(activity_uuid)
        model['data'] = data
      return model
  
  @staticmethod
  def show_activity_info(activity_uuid):
    with xray_recorder.in_subsegment('show_activity_show') as segment:
      sql = db.template('activities', 'show')
      params = { 'uuid': activity_uuid }
      data = db.query_array_json(sql, params)
      return data