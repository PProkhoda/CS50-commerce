# Generated by Django 4.0.6 on 2022-08-15 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_bid_id_alter_categories_id_alter_comments_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='title',
            new_name='Listing',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='user',
            new_name='bider',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='user',
            new_name='commenter',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='watchers',
            new_name='watched_by',
        ),
    ]