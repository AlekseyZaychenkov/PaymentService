import os

from django.db import models
from django.dispatch import receiver


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=2048, null=True, blank=True)
    image_field = models.ImageField(upload_to='images/', null=True, blank=True)


@receiver(models.signals.post_delete, sender=Item)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image_field:
        if os.path.isfile(os.path.join(instance.image_field.path)):
            os.remove(os.path.join(instance.image_field.path))
