from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    created_at = models.DateField(verbose_name='Created at', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Updated at', auto_now=True)
    is_active = models.BooleanField(verbose_name='Is active', default=True)
    tag = models.CharField(verbose_name='Tag', max_length=20, default=None, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User',
                               related_name='news', null=True, blank=True)

    def __str__(self):
        return f'{self.title}, {self.created_at}, {self.is_active}'

    class Meta:
        verbose_name_plural = 'News'
        permissions = (
            ('publish_news', 'Can publish'),
        )


class Comment(models.Model):
    username = models.CharField(max_length=30, verbose_name='Username', blank=True)
    comment_text = models.TextField(verbose_name='Comment text')
    news = models.ForeignKey('News', on_delete=models.CASCADE, verbose_name='News', related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User',
                             related_name='comments', null=True, blank=True)

    def short_comment_text(self):
        result = self.comment_text[:15] + '...'
        return result

    def __str__(self):
        return f'{self.username}, {self.short_comment_text()}'
