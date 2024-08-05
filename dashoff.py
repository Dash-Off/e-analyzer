from flask import Flask, request, jsonify
import threading
from eanalyze import EAnalyze
from dashoff_util import DashOffUtil

app = Flask(__name__)


def validate_mandatory(body, fields):
  for key in body:
      if key not in fields:
         return key, False
  return key, True



def run_server(dashOffId, raw):
  payload = EAnalyze(text=raw).get_result_payload()
  DashOffUtil.update_result(dashOffId, payload)


@app.post('/api/v1/get_scores')
def get_scores():
    if not DashOffUtil.validate_auth(request=request):
       return {"message": "Unauthorized !"}, 401

    body = request.get_json()
    if not body:
       return {"messsage": "Data required"}, 400
    
    key, valid = validate_mandatory(body, ["dashOffId", "raw"])
    if not valid:
       return {"message": f"{key} is mandatory"}
    
    thread = threading.Thread(target=run_server, args=(body["raw"], body["dashOffId"]))
    thread.start()

    return jsonify({"message": f"Job Recieved: {body['dashOffId']}"}), 202