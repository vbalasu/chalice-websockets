# Websocket Connections in Chalice
#### Store connection ids in Postgres and send messages from Python to the browser


```python
import requests, json
```


```python
response = requests.get('http://35.233.160.178:3000/websocket_connections')
response
```




    <Response [200]>




```python
json.loads(response.content)
```




    [{'id': 2,
      'namespace': 'default',
      'connection_id': 'x123',
      'timestamp': '2021-02-09T19:17:27.786349+00:00'},
     {'id': 5,
      'namespace': 'default',
      'connection_id': 'a123',
      'timestamp': '2021-02-09T19:31:00.991105+00:00'},
     {'id': 8,
      'namespace': 'default',
      'connection_id': 'a1234',
      'timestamp': '2021-02-09T19:31:24.973468+00:00'}]




```python
response = requests.delete('http://35.233.160.178:3000/websocket_connections?connection_id=eq.a123')
response
```




    <Response [204]>




```python
response = requests.post('http://35.233.160.178:3000/websocket_connections', json={'connection_id': 'a123'})
response
```




    <Response [201]>




```python
%%time
import boto3
from boto3.session import Session
session = Session(profile_name='vbalasubramaniam_awscli')
connection_id = 'aftycfV1PHcCI7w='
apig = session.client('apigatewaymanagementapi', endpoint_url='https://akpgdwbu6b.execute-api.us-west-2.amazonaws.com/api/')
apig.post_to_connection(Data='hello from Jupyter', ConnectionId=connection_id)
```

    CPU times: user 65.7 ms, sys: 22.8 ms, total: 88.5 ms
    Wall time: 306 ms





    {'ResponseMetadata': {'RequestId': '28035d50-9134-4778-82a7-c218ebd63b02',
      'HTTPStatusCode': 200,
      'HTTPHeaders': {'date': 'Tue, 09 Feb 2021 20:55:18 GMT',
       'content-type': 'application/json',
       'content-length': '0',
       'connection': 'keep-alive',
       'x-amzn-requestid': '28035d50-9134-4778-82a7-c218ebd63b02',
       'x-amz-apigw-id': 'aft8kFLOPHcFwUw=',
       'x-amzn-trace-id': 'Root=1-6022f6b6-05bf1e366c7d53a92ce36005'},
      'RetryAttempts': 0}}


