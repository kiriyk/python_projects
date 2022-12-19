from django.contrib.auth.models import User, PermissionsMixin
from django.db import models

from app_news.models import News


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(max_length=36, blank=True)
    is_verified = models.BooleanField(default=False, blank=True)
    news_number = models.IntegerField(default=0, blank=True)

    @property
    def news_count(self):
        number = News.objects.filter(author=self.user).count()
        print(News.objects.filter(author=self.user).count())
        return number

    class Meta:
        permissions = (
            ('verify_profile', 'Can verify'),
        )
