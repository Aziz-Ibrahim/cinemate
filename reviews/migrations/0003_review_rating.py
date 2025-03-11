# Generated by Django 5.1.6 on 2025-03-11 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_remove_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.FloatField(choices=[(0.5, '★☆☆☆☆ (0.5)'), (1, '★☆☆☆☆ (1)'), (1.5, '★★☆☆☆ (1.5)'), (2, '★★☆☆☆ (2)'), (2.5, '★★★☆☆ (2.5)'), (3, '★★★☆☆ (3)'), (3.5, '★★★★☆ (3.5)'), (4, '★★★★☆ (4)'), (4.5, '★★★★★ (4.5)'), (5, '★★★★★ (5)')], default=0),
            preserve_default=False,
        ),
    ]
