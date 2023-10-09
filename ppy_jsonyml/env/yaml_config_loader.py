import os
import yaml
from ppy_common.ppyc_console_log import Console
from ppy_file_text import FileUtil, TextFileMan
from ppy_jsonyml import YAMLConfigObj


class YAMLConfigLoader:
    PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    default_env_file_name = "env.yml"
    project_root_path: str
    env_file: str = None
    config_obj: YAMLConfigObj = None
    is_print_env: bool = False

    def load(self, env_file: str = None, config_obj: YAMLConfigObj = None, project_root_path: str = PROJECT_ROOT_DIR):
        self.env_file = env_file
        self.project_root_path = project_root_path
        self.config_obj = config_obj
        yaml_dict = self._load_yaml()
        if not yaml_dict and config_obj:
            return config_obj
        elif yaml_dict and config_obj and isinstance(config_obj, YAMLConfigObj):
            return self._map_to_config_object(yaml_dict)
        return config_obj

    def merge_config(self, existing_config):
        yaml_dict = self._load_yaml()
        if yaml_dict:
            for dict_key in yaml_dict:
                if hasattr(existing_config, dict_key):
                    setattr(existing_config, dict_key, yaml_dict[dict_key])

    def _load_yaml(self):
        env_file = self._get_env_file(self.env_file)
        try:
            if not env_file:
                return None
            yaml_content = TextFileMan.get_text_from_file(env_file, exception_message="YAML file not found!")
            return yaml.full_load(yaml_content)
        except Exception as e:
            Console.error(str(e))
        return None

    def _get_env_file(self, env_file: str = None):
        if not env_file:
            env_file_name = self._get_config_file_name()
            env_file = FileUtil.join_path(self.project_root_path, env_file_name)
        if FileUtil.is_exist(env_file):
            return env_file
        return None

    def _get_config_file_name(self):
        env = os.environ.get('env')
        env_name = "Local"
        if env:
            env_name = env

        if not self.is_print_env:
            print("Environment: " + str(env_name))
            self.is_print_env = True

        if env:
            return "env-" + env + ".yml"

        return self.default_env_file_name

    def _map_to_config_object(self, yaml_dict: dict):
        for dict_key in yaml_dict:
            if hasattr(self.config_obj, dict_key):
                setattr(self.config_obj, dict_key, yaml_dict[dict_key])
        return self.config_obj
