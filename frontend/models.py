from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class FrontImage(models.Model):
    image = models.ImageField(upload_to='pages/front')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='images')

