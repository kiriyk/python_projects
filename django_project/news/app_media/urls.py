from django.urls import path

from .import views


urlpatterns = [
    path('upload/', views.FileUploadView.as_view(), name='upload-files'),
    path('goods/', views.TableView.as_view(), name='table-goods'),
    path('documents/', views.DocumentUploadView.as_view(), name='upload-documents'),
    path('multi-upload/', views.MultipleFilesUploadView.as_view(), name='upload-multi-files'),
]
