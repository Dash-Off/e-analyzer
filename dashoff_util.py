import requests
from base64 import encode

class DashOffUtil:
  URL = "http://localhost:3000/api/v1/eval"
  @classmethod
  def get_url(cls, path):
    return f"{cls.URL}{path}"

  @classmethod
  def update_result(cls, dashOffId, payload):
    response = requests.post(cls.get_url(f"/myDashOffs/{dashOffId}/results"), json=payload)
    print(response)
    if response.status_code == 200:
      print(f"Successfully posted results: {dashOffId}")
    else:
      print(f"Failed to post results: {dashOffId}")