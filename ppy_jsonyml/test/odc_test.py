from ppy_jsonyml.converter.od_base import ODBase
from ppy_jsonyml.converter.od_converter import ODConverter
from ppy_jsonyml.converter.yaml_converter import YamlConverter


class Degree(ODBase):
    name: str

    def __init__(self, name=None):
        self.name = name

    def get_globals(self):
        return globals()


class Address(ODBase):
    country: str

    def __init__(self, country: str = None):
        self.country = country

    def get_globals(self):
        return globals()


class Profile(ODBase):
    gender: str
    mobile: str
    address: Address

    def __init__(self, gender: str = None, mobile: str = None):
        self.gender = gender
        self.mobile = mobile

    def get_globals(self):
        return globals()


class Person(ODBase):
    id: int
    firstName: str
    lastName: str
    salary: float
    isMarried: bool
    profile: Profile
    degrees: list[Degree]
    simpleList: list
    simpleDict: dict
    otherAddress: dict[str, Address]

    def get_globals(self):
        return globals()


person1 = Person()
person1.id = 1
person1.firstName = "Touhid"
person1.lastName = "Mia"
person1.salary = 10000
person1.isMarried = True
person1.profile = Profile(gender="Male", mobile="1234")
person1.degrees = [Degree("Primary"), Degree("Secondary"), Degree("Bsc")]
person1.simpleList = ["A", "B", "C", "D"]
person1.simpleDict = {"a": "A", "b": "B"}
person1.otherAddress = {"home": Address("Bangladesh"), "office": Address("Canada")}


od_converter = ODConverter()
dictionary_from_object = od_converter.get_dict(person1, is_ignore_none=True)
print(dictionary_from_object)

dict_object = {
    'id': 1,
    'firstName': 'Touhid',
    'lastName': 'Mia',
    'salary': 10000,
    'isMarried': True,
    'profile': {
        'gender': 'Male', 'mobile': '1234', 'address': None
    },
    'degrees': [
        {'name': 'Primary'},
        {'name': 'Secondary'},
        {'name': 'Bsc'}
    ],
    'simpleList': ['A', 'B', 'C', 'D'],
    'simpleDict': {'a': 'A', 'b': 'B'},
    'otherAddress': {
        'home': {'country': 'Bangladesh'},
        'office': {'country': 'Canada'}
    }
}

person_object: Person = od_converter.get_object(dict_object, Person())
print(person_object)


# YAML Conversion testing
yaml_converter = YamlConverter()
response = yaml_converter.object_to_yaml(person_object)
print(response)

yaml_content = """
id: 1
firstName: Touhid
lastName: Mia
salary: 10000
isMarried: true
profile:
  gender: Male
  mobile: '1234'
  address: null
degrees:
- name: Primary
- name: Secondary
- name: Bsc
simpleList:
- A
- B
- C
- D
simpleDict:
  a: A
  b: B
otherAddress:
  home:
    country: Bangladesh
  office:
    country: Canada
"""

person_yaml = Person()
response = yaml_converter.yaml_to_object(yaml_content, person_yaml)
print(response)
