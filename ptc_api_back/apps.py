from django.apps import AppConfig


class PtcApiBackConfig(AppConfig):
    name = 'ptc_api_back'

    def ready(self):
        import ptc_api_back.signals  # noqa
