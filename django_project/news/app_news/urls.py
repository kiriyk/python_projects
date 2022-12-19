from django.urls import path, include

from .import views

urlpatterns = [
    path('add/', views.NewsAddCreateView.as_view(), name='add-news'),
    path('<int:profile_id>/edit/', views.NewsEditUpdateView.as_view(), name='edit-news'),
    path('', views.NewsList.as_view(), name='news-list'),
    path('<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('news-publish/<int:news_id>', views.NewsPublishView.as_view(), name='news-publish'),
]
