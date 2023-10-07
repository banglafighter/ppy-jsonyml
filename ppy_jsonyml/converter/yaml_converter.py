import os
from os.path import exists, dirname
from typing import Union
import yaml
from ppy_jsonyml.converter.od_base import ODBase
from ppy_jsonyml.converter.od_converter import ODConverter


class YamlConverter:
    od_converter = ODConverter()

    def dict_to_yaml(self, data: dict) -> Union[str, None]:
        try:
            return yaml.dump(data, sort_keys=False, allow_unicode=True)
        except Exception as e:
            return None

    def yaml_to_dict(self, yaml_content: str, default=None) -> Union[dict, None]:
        try:
            return yaml.full_load(yaml_content)
        except Exception as e:
            return default

    def object_to_yaml(self, od_object: ODBase, is_ignore_none=False) -> Union[str, None]:
        dict_data = self.od_converter.get_dict(od_object=od_object, is_ignore_none=is_ignore_none)
        if dict_data:
            return self.dict_to_yaml(dict_data)
        return None

    def yaml_to_object(self, yaml_content: str, od_object: ODBase, default=None) -> Union[ODBase, None]:
        dict_data = self.yaml_to_dict(yaml_content)
        if dict_data:
            return self.od_converter.get_object(dict_data, od_object=od_object)
        return default

    def write_yaml_object_to_file(self, file_path_with_name: str, od_object: ODBase, is_ignore_none=False) -> bool:
        if not file_path_with_name or not od_object:
            return False

        yaml_content = self.object_to_yaml(od_object, is_ignore_none)
        if not yaml_content:
            return False
        return self.write_yaml_content_to_file(file_path_with_name, yaml_content)

    def write_yaml_dict_to_file(self, file_path_with_name: str, data_dict: dict) -> bool:

        if not file_path_with_name or not data_dict:
            return False

        yaml_content = self.dict_to_yaml(data_dict)
        if not yaml_content:
            return False
        return self.write_yaml_content_to_file(file_path_with_name, yaml_content)

    def write_yaml_content_to_file(self, file_path_with_name: str, yaml_content: str) -> bool:
        if not file_path_with_name:
            return False

        try:
            if exists(file_path_with_name):
                os.remove(file_path_with_name)

            directory = dirname(file_path_with_name)
            if not os.path.exists(directory):
                os.makedirs(directory)

            stream = open(file_path_with_name, 'w', encoding="utf-8")
            stream.write(yaml_content)
            stream.close()
            return True
        except Exception as e:
            return False

    def read_yaml_object_from_file(self, file_path_with_name: str, od_object: ODBase, default=None) -> Union[ODBase, None]:
        yaml_content = self.read_yaml_content_from_file(file_path_with_name)
        return self.yaml_to_object(yaml_content, od_object, default=default)

    def read_yaml_dict_from_file(self, file_path_with_name: str, default=None) -> Union[ODBase, None]:
        yaml_content = self.read_yaml_content_from_file(file_path_with_name)
        return self.yaml_to_dict(yaml_content, default=default)

    def read_yaml_content_from_file(self, file_path_with_name: str, default=None) -> Union[str, None]:
        if not exists(file_path_with_name):
            return default

        try:
            stream = open(file_path_with_name, 'r', encoding="utf-8")
            return stream.read()
        except Exception as e:
            return default

    def validate_yaml(self, yaml_content):
        try:
            return yaml.safe_load(yaml_content)
        except yaml.YAMLError as exception:
            raise exception

    def is_validate_yaml(self, yaml_content) -> bool:
        try:
            self.validate_yaml(yaml_content)
            return True
        except yaml.YAMLError as exception:
            return False
