# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def document_utilities_view(request):
    context = {}
    return render(request, 'document_utilities/document_utilities.html', context)
