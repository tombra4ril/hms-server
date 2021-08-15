from django.db import migrations
import json
from core.common import get_category

def initial_data(apps, schema_editor):
    # we cannot import the user model directly as it may be a newer version than this migration expects. we will use the historical version
    Users_Table = apps.get_model("category", "Category")
    #load initial_users json file
    users = get_category()
    for name in users["names"]:
        users_row = Users_Table(name=name)
        users_row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_data)
    ]
