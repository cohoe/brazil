Brazil
======

Plugins:
* serverless-python-requrements
* serverless-offline
* serverless-dynamodb-local

Random Commands
---------------
```
aws --profile localtest --region us-east-2 dynamodb list-tables --endpoint-url http://127.0.0.1:8000
```

```
sls dynamodb migrate
sls start offline (must be in the right venv)
```