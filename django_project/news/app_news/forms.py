from django import forms
from django.forms import widgets

from app_news.models import *


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'comment_text']


class FilterNews(forms.Form):
    CHOICES = [('0', 'Date by ascending'), ('1', 'Date by descending')]

    def choices():
        tag = News.objects.values('tag').distinct()
        choices_list = [(idx, elm.get('tag')) for idx, elm in enumerate(tag)]
        return choices_list

    name = forms.ChoiceField(widget=forms.RadioSelect, choices=choices, label='Filter by')
    ordering = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label='Order by')


