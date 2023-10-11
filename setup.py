from setuptools import setup, find_packages
import os
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
README = (CURRENT_DIR / "README.md").read_text()

env = os.environ.get('source')


def get_dependencies():
    dependency = ["PyYAML==6.0.1"]

    if env and env == "code":
        return dependency

    return dependency + ["ppy-common", "ppy-file-text"]


setup(
    name='ppy-jsonyml',
    version='0.0.2',
    url='https://github.com/problemfighter/ppy-jsonyml',
    license='Apache 2.0',
    author='Problem Fighter',
    author_email='problemfighter.com@gmail.com',
    description='PWeb Python JSON & YAML is a library which help to serialize and deserialize Object as well as help to load configuration',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_dependencies(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ]
)
