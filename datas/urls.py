from .views import RecognitionListView
from django.conf.urls import include, url

urlpatterns = [
    url('recognition', RecognitionListView.as_view()),
]
