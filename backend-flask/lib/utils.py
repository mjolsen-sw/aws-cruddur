from flask import jsonify

def model_json(model):
  if len(model['errors']) > 0:
    return jsonify(model['errors']), 422
  else:
    return jsonify(model['data']), 200