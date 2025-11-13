import json
import importlib.util
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'app.py'))
spec = importlib.util.spec_from_file_location('app_module', APP_PATH)
app_module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(app_module)  # type: ignore
app = getattr(app_module, 'app')
from app.model import db


def test_register_login_status_validate():
  with app.app_context():
    db.create_all()
  client = app.test_client()

  username = f"testuser_{__import__('random').randint(100000, 999999)}"
  email = f"{username}@example.com"
  # register
  resp = client.post(
    "/api/auth/register",
    data=json.dumps({
      "username": username,
      "nickname": "Tester",
      "email": email,
      "password": "pass1234"
    }),
    content_type="application/json",
  )
  data = resp.get_json()
  print('REGISTER RESP:', resp.status_code, resp.get_data(as_text=True))
  assert resp.status_code == 200
  assert data["code"] == 200

  # login
  resp = client.post(
    "/api/auth/login",
    data=json.dumps({"username": username, "password": "pass1234"}),
    content_type="application/json",
  )
  login_data = resp.get_json()
  assert resp.status_code == 200
  assert login_data["code"] == 200
  token = login_data["data"]["token"]
  assert isinstance(token, str) and len(token) > 10

  # status
  resp = client.get(
    "/api/auth/status",
    headers={"Authorization": f"Bearer {token}"},
  )
  status_data = resp.get_json()
  print('STATUS RESP:', resp.status_code, resp.get_data(as_text=True))
  assert resp.status_code == 200
  assert status_data["code"] == 200
  assert status_data["data"]["is_authenticated"] is True

  # validate
  resp = client.post(
    "/api/auth/validate",
    headers={"Authorization": f"Bearer {token}"},
    data=json.dumps({"token": token}),
    content_type="application/json",
  )
  validate_data = resp.get_json()
  assert resp.status_code == 200
  assert validate_data["code"] == 200
  assert validate_data["data"]["valid"] is True
