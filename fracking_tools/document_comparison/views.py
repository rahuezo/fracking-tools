# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from utils.files import ExtensionHandler
from utils.document_comparison import compair

import os
import re
import csv


def clean_text(s):
    return ' '.join(' '.join(re.findall(r'[a-zA-Z0-9]+', s)).split())


def document_comparison_view(request):
    context = {}
    return render(request, 'document_comparison/document_comparison.html', context)


def compare_documents_view(request):
    if request.method == 'POST':
        documents = request.FILES.getlist('comparison-documents')

        results = []

        for i in xrange(len(documents)):
            for j in xrange(i + 1, len(documents)):

                content1, content2 = ExtensionHandler(documents[i]).get_content(), ExtensionHandler(documents[j]).get_content()
                documents[i].seek(0)
                documents[j].seek(0)

                try:
                    result = [documents[i].name, documents[j].name] + compair(content1, content2)
                    results.append(result)
                except Exception as e:
                    print "Error: ", e
                    result = [documents[i].name, documents[j].name, 'Error', 'Error']
                    results.append(result)

        fs = FileSystemStorage()
        output_csv_path = "{0}.csv".format(os.path.join(fs.location, clean_text(request.POST.get('comparison-output-csv-name'))))

        header = ['File A', 'File B', 'Cosine Similarity', 'Jaccard Similarity']

        with open(output_csv_path, 'wb') as csv_file:
            writer = csv.writer(csv_file, delimiter=str(u',').encode('utf-8'))
            writer.writerow(header)
            for result in results:
                writer.writerow(result)

        with open(output_csv_path, 'rb') as csv_file:
            response = HttpResponse(csv_file.read())
            response['content_type'] = 'text/csv'
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.split(output_csv_path)[1])
    return response #redirect('document_utilities:doccomp')
