from django.shortcuts import render
from django.views.generic import ListView
from .models import Recognition


class RecognitionListView(ListView):

    model = Recognition
    template_name = 'recognition_list.html'
