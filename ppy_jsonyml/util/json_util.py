import ast
import json
from ppy_common import Console


class JsonUtil:

    @staticmethod
    def str_to_obj(json_string: str, default=None):
        try:
            if json_string:
                json_string = json.dumps(ast.literal_eval(json_string))
                return json.loads(json_string)
        except Exception as e:
            Console.log(f"json str_to_obj error: {e}")
        return default

    @staticmethod
    def get_dict(json_string: str, default=None):
        json_object = JsonUtil.str_to_obj(json_string, default)
        if isinstance(json_object, dict):
            return json_object
        return None

    @staticmethod
    def get_list(json_string: str, default=None):
        json_object = JsonUtil.str_to_obj(json_string, default)
        if isinstance(json_object, list):
            return json_object
        return None
