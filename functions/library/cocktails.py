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


def list_by_alpha(event, context):
    alpha = event['pathParameters']['alpha']

    redis = RedisConnector()
    try:
        cocktail_name_list = json.loads(redis.get(barbados.config.cache.cocktail_name_list_key))

        cocktail_names = []
        for entry in cocktail_name_list:
            if entry['display_name'].upper().startswith(alpha.upper()):
                cocktail_names.append(entry)

        response = {
            'statusCode': 200,
            'body': json.dumps(cocktail_names)
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


def build_search_cache(event, context):
    redis = RedisConnector()
    index_scan_results = CocktailModel.name_index.scan()
    results = [result.attribute_values for result in index_scan_results]
    redis.set(barbados.config.cache.cocktail_name_list_key, json.dumps(results))