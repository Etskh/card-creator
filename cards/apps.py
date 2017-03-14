from django.apps import AppConfig


class CardsConfig(AppConfig):
    name = 'cards'

    version_major = 0
    version_minor = 0
    version_release = 1

    version_full = '.'.join([
        str(version_major),
        str(version_minor),
        str(version_release),
    ])

