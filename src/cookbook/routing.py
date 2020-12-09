from django.urls import path

from .consumers import SubscriptionConsumer

websocket_urlpatterns = [path("graphql/", SubscriptionConsumer.as_asgi())]
