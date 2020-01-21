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

    if len(alpha) > 1:
        return ({
            'statusCode': 400,
            'body': 'Only pass a single character.'
        })

    redis = RedisConnector()
    try:
        search_index = json.loads(redis.get(barbados.config.cache.cocktail_name_list_key))

        response = {
            'statusCode': 200,
            'body': json.dumps(_get_key_from_cache(search_index, alpha))
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


# def build_search_cache(event, context):
#     redis = RedisConnector()
#     index_scan_results = CocktailModel.name_index.scan()
#     results = [result.attribute_values for result in index_scan_results]
#     redis.set(barbados.config.cache.cocktail_name_list_key, json.dumps(results))

def build_search_cache(event, context):
    redis = RedisConnector()
    index_scan_results = CocktailModel.name_index.scan()

    index = {}
    for result in index_scan_results:
        key_alpha = result.slug[0].upper()
        if key_alpha not in index.keys():
            index[key_alpha] = [result.attribute_values]
        else:
            index[key_alpha].append(result.attribute_values)

    redis.set(barbados.config.cache.cocktail_name_list_key, json.dumps(index))


def _get_key_from_cache(cache, key):
    if key == '#':
        search_results = []
        for i in range(0,10):
            try:
                search_results += cache[str(i)]
            except KeyError:
                pass
    else:
        try:
            search_results = cache[key.upper()]
        except KeyError:
            search_results = []

    return search_results
