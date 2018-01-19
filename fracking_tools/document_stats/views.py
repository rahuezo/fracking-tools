# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from utils.tag_docs_for_keywords import KeywordTagger
from utils.files import csplit
from zipfile import ZipFile

from utils.stats import DocumentStats

import os
import re
import csv


def unspace(s):
    return s.strip()


def clean_text(s):
    return ' '.join(' '.join(re.findall(r'[a-zA-Z0-9]+', s)).split())


def document_stats_view(request):
    context = {}

    return render(request, 'document_stats/document_stats.html', context)


def analyze_documents_view(request):
    if request.method == 'POST':
        keywords_type = request.POST.get('keywords-type')
        documents_to_analyze = request.FILES.getlist('analyze-documents')

        if keywords_type == 'file':
            keywords_file = request.FILES.getlist('file-keyword-list')[0]
            keywords = map(unspace, keywords_file.read().split(','))
        else:
            manual_keyword_list = request.POST.get('manual-keyword-list')
            keywords = map(unspace, manual_keyword_list.split(','))

        stats = []

        for document in documents_to_analyze:
            ds = DocumentStats(document, keywords)
            stats.append([document.name] + ds.compute_all())

        fs = FileSystemStorage()
        output_csv_path = os.path.join(fs.location, "{0}.csv".format(clean_text(request.POST.get('output-csv-name'))))

        header = ['File Name', 'Reading Level', 'Word Count'] + [kw.title() for kw in keywords] + \
                 ['Polarity', 'Subjectivity', 'Classification', 'P_POS', 'P_NEG']

        with open(output_csv_path, 'wb') as csv_file:
            writer = csv.writer(csv_file, delimiter=str(u',').encode('utf-8'))
            writer.writerow(header)
            for stat in stats:
                writer.writerow(stat)

        with open(output_csv_path, 'rb') as csv_file:
            response = HttpResponse(csv_file.read())
            response['content_type'] = 'text/csv'
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.split(output_csv_path)[1])

        return response
    return redirect('document_utilities:docstats')
