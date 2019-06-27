from django.shortcuts import render
from django.views.generic import ListView
from .models import Recognition


class RecognitionListView(ListView):

    model = Recognition
    template_name = 'recognition_list.html'

    def get_queryset(self, queryset=None):
        return Recognition.objects.order_by('pub_date').reverse()[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
