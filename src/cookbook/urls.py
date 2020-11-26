from django.contrib import admin
from django.urls import include, path

from graphene_django.views import GraphQLView

from .views import index

urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]
