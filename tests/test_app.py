from chalice.test import Client
from app import app

def test_send_message():
  with Client(app) as client:
    response = client.http.get('/send_message?message=HelloWorld')
    assert response.status_code == 200

def test_run_command():
  import json
  with Client(app) as client:
    response = client.http.post('/run_command', headers={'Content-Type': 'application/json'}, body=json.dumps({'command': ['ls', '-l', '/']}))
    assert response.status_code == 200