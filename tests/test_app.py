from chalice.test import Client
from app import app

def test_send_message():
  with Client(app) as client:
    response = client.http.get('/send_message?message=HelloWorld')
    assert response.status_code == 200