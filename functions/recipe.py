import json
import barmenu
import barmenu.factories

def get(event, context):
    slug = event['pathParameters']['slug']

    return ({
        "statusCode": 200,
        "body": "The slug is %s and %s" % (slug, barmenu.factories.CocktailFactory)
    })
