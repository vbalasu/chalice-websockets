from boto3.session import Session
from chalice import Chalice
import requests, json

app = Chalice(app_name='chalice-websockets')
app.experimental_feature_flags.update(['WEBSOCKETS'])
app.websocket_api.session = Session()

@app.on_ws_connect()
def connect(event):
    response = requests.post('http://35.233.160.178:3000/websocket_connections', json={'connection_id': event.connection_id})
    print('New connection: %s' % event.connection_id, response.content)

@app.on_ws_message()
def message(event):
    app.websocket_api.send(event.connection_id, event.body)
    print('%s: %s' % (event.connection_id, event.body))

@app.route('/send_message')
def send_message():
    response = requests.get('http://35.233.160.178:3000/websocket_connections?namespace=eq.default')
    session = Session()
    apig = session.client('apigatewaymanagementapi', endpoint_url='https://akpgdwbu6b.execute-api.us-west-2.amazonaws.com/api/')
    for connection in response.json():
        apig.post_to_connection(Data=app.current_request.query_params['message'], ConnectionId=connection['connection_id'])
    return True

# USAGE: http post http://127.0.0.1:8000/run_command command:='["ls", "-l"]'
# USAGE: http post $(chalice url)run_command command:='["env"]'
@app.route('/run_command', methods=['POST'])
def run_command():
    import subprocess
    #print(app.current_request.json_body)
    return subprocess.check_output(app.current_request.json_body['command']).decode()

@app.on_ws_disconnect()
def disconnect(event):
    response = requests.delete(f'http://35.233.160.178:3000/websocket_connections?connection_id=eq.{event.connection_id}')
    print('%s disconnected' % event.connection_id)

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
