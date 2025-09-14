from typing import Any, Dict
from pydantic import BaseModel, HttpUrl


def serialize_for_mongo(model: BaseModel) -> Dict[str, Any]:
    """
    Converts a Pydantic model into a dict that can be safely inserted into MongoDB.
    - Converts HttpUrl fields to string
    """
    data = model.model_dump()

    def convert(obj):
        if isinstance(obj, HttpUrl):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(i) for i in obj]
        else:
            return obj

    return convert(data)
