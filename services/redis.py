from database import r
import json

def redis_set(key, value, ex=None):
    r.set(key, json.dumps(value), ex=ex)

def redis_get(key):
    value = r.get(key)
    if value is not None:
        return json.loads(value)
    return None

def redis_delete(key):
    r.delete(key)