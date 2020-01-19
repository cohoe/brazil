import json
from barbados.models import CocktailModel
from barbados.factories import CocktailFactory


def get(event, context):
    slug = event['pathParameters']['slug']

    try:
        result = CocktailModel.query(hash_key=slug).next()
        object = CocktailFactory.model_to_obj(result)

        response = {
            'statusCode': 200,
            'body': json.dumps(object.serialize())
        }
    except StopIteration:
        response = {
            'statusCode': 404
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': str(e)
        }

    return response
