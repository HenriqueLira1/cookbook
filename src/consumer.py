import os
import ssl

import faust
from faust.sensors.datadog import DatadogMonitor

os.environ.setdefault("FAUST_LOOP", "eventlet")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookbook.settings.local")

app = faust.App(
    "cookbook",
    autodiscover=True,
    origin="cookbook",
)


@app.on_configured.connect
def configure_from_settings(app, conf, **kwargs):
    from django.conf import settings

    brokers = [f"kafka://{broker}" for broker in settings.KAFKA_BROKERS_URL.split(",")]
    conf.broker = brokers

    conf.logging_config = settings.LOGGING

    if settings.KAFKA_USE_SSL:
        ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
        conf.broker_credentials = ssl_context

    if settings.DATADOG_HOST:
        conf.monitor = DatadogMonitor(settings.DATADOG_HOST)


def main():
    app.main()


if __name__ == "__main__":
    main()
