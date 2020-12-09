from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

from .views import index

urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG))),
]
