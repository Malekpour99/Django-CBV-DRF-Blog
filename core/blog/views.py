from django.shortcuts import render

from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    Renders index page of the blog
    """

    template_name = "blog/index.html"
