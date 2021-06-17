from django.contrib.auth import get_user_model
from django.db import models

CustomUser = get_user_model()

class ProfileProducer(models.Model):
    slug = models.SlugField(unique=False, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile_producer')
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return f'{self.user.email}'

    def save(self, *args, **kwargs):
        to_slug = str(self.user.username)
        self.slug = to_slug
        super().save(*args, **kwargs)


class ProfileCustomer(models.Model):
    slug = models.SlugField(unique=False, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile_customer')
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        to_slug = str(self.user.username)
        self.slug = to_slug
        super().save(*args, **kwargs)
