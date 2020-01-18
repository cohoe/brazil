import json


def get(event, context):
    slug = event['pathParameters']['slug']

    return ({
        "statusCode": 200,
        "body": "The slug is %s" % slug
    })
