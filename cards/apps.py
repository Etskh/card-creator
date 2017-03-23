from django.apps import AppConfig
import json

with open('package.json') as data_file:
    version = json.load(data_file)['version']


class CardsConfig(AppConfig):
    name = 'cards'
    package_path = 'package.json'

    version_full = version

