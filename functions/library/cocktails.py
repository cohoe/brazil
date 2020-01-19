import json
import barbados.config
from barbados.models import CocktailModel
from barbados.factories import CocktailFactory
from barbados.connectors import RedisConnector


def _list(event, context):
    redis = RedisConnector()
    try:
        cocktail_name_list = redis.get(barbados.config.cache.cocktail_name_list_key)
        response = {
            'statusCode': 200,
            'body': json.dumps(json.loads(cocktail_name_list))
        }
    except KeyError:
        response = {
            'statusCode': 502,
            'body': 'Cache empty or other Redis error.'
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': str(e)
        }

    return response


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
