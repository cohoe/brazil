import json


def get(event, context):

    slug = event['pathParameters']['slug']

    return {
        "statusCode": 200,
        "body": json.dumps({
            "slug": slug,
            "event": event
        }),
        # "body": "Slug was %s" % slug
    }
