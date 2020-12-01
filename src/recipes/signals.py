from django.db.models.signals import post_delete, post_save

from graphene_subscriptions.signals import (
    post_delete_subscription,
    post_save_subscription,
)

from .models import Ingredient, Recipe

post_save.connect(
    post_save_subscription, sender=Ingredient, dispatch_uid="ingredient_post_save"
)
post_delete.connect(
    post_delete_subscription, sender=Ingredient, dispatch_uid="ingredient_post_delete"
)


post_save.connect(
    post_save_subscription, sender=Recipe, dispatch_uid="recipe_post_save"
)
post_delete.connect(
    post_delete_subscription, sender=Recipe, dispatch_uid="recipe_post_delete"
)
