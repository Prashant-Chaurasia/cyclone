import decimal
import json
from datetime import datetime

# https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat() + "Z"
        elif hasattr(obj, '__class__'):
            if hasattr(obj, 'serialize'):
                return obj.serialize()
            else:
                return None
        return json.JSONEncoder.default(self, obj)


def serialize(instance, **kwargs):
    if isinstance(instance, str):
        return instance
    return json.dumps(instance, cls=ComplexEncoder, **kwargs)
