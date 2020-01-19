import json
import barbados
import barbados.factories

def get(event, context):
    slug = event['pathParameters']['slug']

    return ({
        "statusCode": 200,
        "body": "The slug is %s and %s" % (slug, barbados.factories.CocktailFactory)
    })
