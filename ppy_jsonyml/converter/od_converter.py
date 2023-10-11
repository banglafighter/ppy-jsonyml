from typing import List, Dict
from ppy_jsonyml.converter.od_base import ODBase, ODAttributeDetails
from ppy_jsonyml.converter.od_util import ODUtil


class ODConverter:

    def _init_od_object(self, data, od_attr_details: ODAttributeDetails):
        if not od_attr_details.objectClass:
            return None
        else:
            return self.get_object(data=data, od_object=od_attr_details.objectClass())

    def _init_od_dict_object(self, data_dict: dict, od_attr_details: ODAttributeDetails):
        od_object_dict = {}
        for data_name in data_dict:
            response = self._init_od_object(data=data_dict[data_name], od_attr_details=od_attr_details)
            if response:
                od_object_dict[data_name] = response

        if od_object_dict:
            return od_object_dict

        return None

    def _init_od_list_object(self, data_list: list, od_attr_details: ODAttributeDetails):
        od_object_list = []
        for data in data_list:
            response = self._init_od_object(data, od_attr_details=od_attr_details)
            if response:
                od_object_list.append(response)

        if od_object_list:
            return od_object_list

        return None

    def _set_value_to_object(self, attribute_name: str, data: dict, data_and_type_map: dict, od_object: ODBase):
        if attribute_name not in data_and_type_map:
            return od_object

        od_attr_details: ODAttributeDetails = data_and_type_map[attribute_name]
        value = None
        if od_attr_details.typeName == "dict" and od_attr_details.objectType == "ODBase" and isinstance(data[attribute_name], dict):
            value = self._init_od_dict_object(data_dict=data[attribute_name], od_attr_details=od_attr_details)
        elif od_attr_details.typeName == "list" and od_attr_details.objectType == "ODBase" and isinstance(data[attribute_name], list):
            value = self._init_od_list_object(data_list=data[attribute_name], od_attr_details=od_attr_details)
        elif od_attr_details.objectType == "ODBase":
            value = self._init_od_object(data=data[attribute_name], od_attr_details=od_attr_details)
        else:
            value = data[attribute_name]

        if value and od_attr_details.typeName == "str":
            value = str(value)
        setattr(od_object, attribute_name, value)
        return od_object

    def _handle_internal_list(self, list_data, is_ignore_none=False):
        response = []
        for item in list_data:
            item = self._process_value(item, is_ignore_none)
            response.append(item)
        return response

    def _handle_internal_dict(self, dict_data, is_ignore_none=False):
        response = {}
        for item_name in dict_data:
            response[item_name] = self._process_value(dict_data[item_name], is_ignore_none)
        return response

    def _process_value(self, value, is_ignore_none=False):
        if not value:
            return value
        if isinstance(value, ODBase):
            value = self.get_dict(od_object=value, is_ignore_none=is_ignore_none)
        elif isinstance(value, List):
            value = self._handle_internal_list(list_data=value, is_ignore_none=is_ignore_none)
        elif isinstance(value, Dict):
            value = self._handle_internal_dict(dict_data=value, is_ignore_none=is_ignore_none)
        return value

    def get_dict(self, od_object: ODBase, is_ignore_none=False, exclude: list = None):
        response_dict = {}
        data_and_type_map = ODUtil.get_class_attr_details(od_object)

        for field_name in data_and_type_map:
            if exclude and field_name in exclude:
                continue

            value = None
            if hasattr(od_object, field_name):
                value = getattr(od_object, field_name, None)
                value = self._process_value(value, is_ignore_none)

            if not is_ignore_none:
                response_dict[field_name] = value

            elif is_ignore_none and value:
                response_dict[field_name] = value

        return response_dict

    def get_object(self, data: dict, od_object: ODBase, exclude: list = None):
        if not data or not od_object:
            return None

        data_and_type_map = ODUtil.get_class_attr_details(od_object)

        for attribute_name in data:
            if exclude and attribute_name in exclude:
                continue
            od_object = self._set_value_to_object(attribute_name=attribute_name, data=data, data_and_type_map=data_and_type_map, od_object=od_object)

        for attribute_name in data_and_type_map:
            if not hasattr(od_object, attribute_name):
                setattr(od_object, attribute_name, None)
        return od_object
