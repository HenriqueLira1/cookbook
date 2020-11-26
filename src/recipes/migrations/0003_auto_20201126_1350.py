# Generated by Django 3.1.3 on 2020-11-26 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0002_recipe_ingredients"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                related_name="recipes", to="recipes.Ingredient"
            ),
        ),
    ]
