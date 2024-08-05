import requests
import hmac
import hashlib
from base64 import b64encode
import os
class DashOffUtil:
  URL = os.environ.get('MAIN_APP')
  SECRET = os.environ.get("MAIN_APP_SECRET")
  WHITELIST_IPS = os.environ.get("WHITELIST_IPS", "").split(",")
  @classmethod
  def get_url(cls, path):
    return f"{cls.URL}{path}"
  
  @classmethod
  def get_x_auth(cls, payload):
    sign_string = "signed,"
    for key in payload:
      sign_string += f"{key},"
    return b64encode(
      hmac.new(cls.SECRET.encode(), sign_string.encode(), hashlib.sha256).hexdigest().encode()
    ).decode()
  
  @classmethod
  def validate_auth(cls, request):
    headers = request.headers
    ip = request.remote_addr
    payload = request.get_json()

    print(ip)
    print(payload)
    print(headers)
    print(headers["x-auth"])
    print(headers.get("X-AUTH"))
    if "X-AUTH" not in headers:
      return False
    if ip not in cls.WHITELIST_IPS:
      return False
    
    X_AUTH = headers["X-AUTH"]
    signature = cls.get_x_auth(payload)
    print(signature)
    return X_AUTH == signature
    

  @classmethod
  def update_result(cls, dashOffId, payload):
    response = requests.post(cls.get_url(f"/myDashOffs/{dashOffId}/results"), json=payload, headers={"X-AUTH": cls.get_x_auth(payload=payload)})

    if response.status_code == 200:
      print(f"Successfully posted results: {dashOffId}")
    else:
      print(f"Failed to post results: {dashOffId}")