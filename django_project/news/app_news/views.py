from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, reverse
from django.views import View, generic
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from app_news.models import *
from app_news.forms import NewsForm, CommentForm, FilterNews


class NewsAddCreateView(PermissionRequiredMixin, generic.edit.CreateView):
    model = News
    fields = ['title', 'description', 'tag']
    permission_required = 'app_news.add_news'
    permission_denied_message = 'You have no permission to add news'
    login_url = '/users/login/'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        title, descr = request.POST.get('title'), request.POST.get('description')
        tag = request.POST.get('tag') if request.POST.get('tag') else None
        News.objects.create(title=title, description=descr, is_active=False, tag=tag, author=user)

        return redirect('news-list')


class NewsEditUpdateView(PermissionRequiredMixin, generic.edit.UpdateView):
    model = News
    fields = '__all__'
    pk_url_kwarg = 'profile_id'
    permission_required = 'app_news.change_news'
    permission_denied_message = 'You have no permission to change news'
    login_url = '/users/login/'

    def get_success_url(self):
        return reverse('edit-news', args=(self.object.pk,))


class NewsList(View):
    def get(self, request):
        news_list = News.objects.filter(is_active=True).order_by('-created_at')
        radio_form = FilterNews
        can_publish_button = False
        if request.user.has_perm('app_news.can_publish'):
            can_publish_button = True
            news_list = News.objects.order_by('-created_at')
        return render(request, 'news/news.html', context={'news_list': news_list,
                                                          'radio_form': radio_form,
                                                          'can_publish': can_publish_button})

    def post(self, request):
        order_dict = {'0': 'created_at', '1': '-created_at'}
        radio_form = FilterNews
        radio_form_post = FilterNews(request.POST)
        if radio_form_post.is_valid():
            filter_by = FilterNews.choices()[int(radio_form_post.cleaned_data.get('name'))]
            order_by = FilterNews.CHOICES[int(radio_form_post.cleaned_data.get('ordering'))]
            news_list = News.objects.filter(tag=filter_by[1]).order_by(order_dict.get(order_by[0]))
            return render(request, 'news/news.html', context={'news_list': news_list, 'radio_form': radio_form_post})

        return render(request, 'news/news.html', context={'radio_form': radio_form})


class NewsDetailView(generic.DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        return context

    def post(self, request, **kwargs):
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_record = comment_form.save(commit=False)
            if request.user.is_authenticated:
                new_record.username = request.user.username
                new_record.user = request.user

            new_record.news = self.get_object()
            new_record.save()
            return redirect('news-detail', pk=self.get_object().id)

        return render(request, 'app_news/news_detail.html')


class NewsPublishView(PermissionRequiredMixin, View):
    model = News
    template_name = 'news/publish_news.html'
    pk_url_kwarg = 'news_id'
    fields = ['title', 'is_active']
    permission_required = 'app_news.publish_news'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        news_id = kwargs.get('news_id')
        news = News.objects.get(id=news_id)
        news.is_active = True
        news.save()
        return redirect('news-list')
