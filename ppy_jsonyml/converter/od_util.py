import inspect
from ppy_jsonyml.converter.od_base import ODAttributeDetails, ODBase


class ODUtil:

    @staticmethod
    def set_none_primitive_data_details(attribute_details: ODAttributeDetails, object_class):
        if issubclass(object_class, ODBase):
            attribute_details.objectType = "ODBase"
            attribute_details.objectClass = object_class
        else:
            attribute_details.objectType = "Unknown"
        return attribute_details

    @staticmethod
    def get_collection_args(object_class, index):
        if hasattr(object_class, "__args__") and len(getattr(object_class, "__args__")) > index:
            return getattr(object_class, "__args__")[index]
        return None

    @staticmethod
    def set_attribute_type(attribute_details: ODAttributeDetails, class_object):
        if attribute_details.typeName in ["str", "int", "float", "bool"]:
            attribute_details.objectType = "primitive"
        else:
            try:
                attribute_details.objectType = "Unknown"
                for attrs in inspect.getmembers(class_object):
                    if len(attrs) == 2 and attrs[0] == "__annotations__":
                        all_attributes = attrs[1]
                        object_class = all_attributes[attribute_details.attributeName]
                        if attribute_details.typeName == "list":
                            class_name = ODUtil.get_collection_args(object_class, index=0)
                            if class_name:
                                attribute_details = ODUtil.set_none_primitive_data_details(attribute_details=attribute_details, object_class=class_name)
                        elif attribute_details.typeName == "dict":
                            value_class_name = ODUtil.get_collection_args(object_class, index=1)
                            if value_class_name:
                                attribute_details = ODUtil.set_none_primitive_data_details(attribute_details=attribute_details, object_class=value_class_name)

                            key_class_name = ODUtil.get_collection_args(object_class, index=0)
                            if key_class_name:
                                attribute_details.dictKeyType = key_class_name.__name__
                        else:
                            attribute_details = ODUtil.set_none_primitive_data_details(attribute_details=attribute_details, object_class=object_class)
                    break
            except:
                pass
        return attribute_details

    @staticmethod
    def get_class_attr_details(class_object):
        attribute_details_map: dict[str, ODAttributeDetails] = {}
        for attrs in inspect.getmembers(class_object):
            if len(attrs) == 2 and attrs[0] == "__annotations__":
                all_attributes = attrs[1]
                for attr_name in all_attributes:
                    attribute_details = ODAttributeDetails()
                    attribute_details.attributeName = attr_name
                    attribute_details.typeName = all_attributes[attr_name].__name__
                    attribute_details = ODUtil.set_attribute_type(attribute_details, class_object)
                    attribute_details_map[attr_name] = attribute_details
                break
        return attribute_details_map
