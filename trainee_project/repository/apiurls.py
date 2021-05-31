from django.urls import path
from .apiviews import FileManage

urlpatterns = [
    path('', FileManage.as_view(), name='list_users'),
]
