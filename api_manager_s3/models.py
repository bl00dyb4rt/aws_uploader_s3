from django.db import models


class Images(models.Model):
    name = models.CharField(max_length=200)
    full_path = models.CharField(max_length=200)
    hash_name = models.CharField(max_length=200)
    status = models.IntegerField()
    upload_count = models.IntegerField()

    def __str__(self):
        return '%d: %s' % (self.order, self.title)

    def save_image(self, name, full_path, hash_name, status=1, upload_count=1):
        image = Images(name=name, full_path=full_path, hash_name=hash_name, status=status, upload_count=upload_count)
        image.save()
        return image

    def list_images_url(self):
        list_images = Images.objects.values_list('id', 'full_path')
        return list_images
