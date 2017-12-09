# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def document_tagging_view(request):
    context = {}
    return render(request, 'document_tagging/document_tagging.html', context)
