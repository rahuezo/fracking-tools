# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib import messages

from zipfile import ZipFile
from utils.matrices import AdjacencyMatrix, df2csv, get_adjmat_name

import csv
import re
import os


def clean_text(s):
    return ' '.join(' '.join(re.findall(r'[a-zA-Z0-9]+', s)).split())


def network_builder_view(request):
    context = {}
    return render(request, 'network_builder/network_builder.html')


def events_network_view(request):
    context = {}
    return render(request, 'network_builder/events_network.html', context)


def pairs_network_view(request):
    context = {}
    return render(request, 'network_builder/pairs_network.html', context)


def build_event_networks(request):
    if request.method == 'POST':

        files = request.FILES.getlist('event-csvs')

        matrices = {}

        for f in files:
            rows = [row for row in csv.reader(f, delimiter=str(u',').encode('utf-8'))]
            matrices[get_adjmat_name(f.name)] = AdjacencyMatrix(rows).build()

        fs = FileSystemStorage()
        output_zip_path = os.path.join(fs.location, clean_text(request.POST.get('events-output-zip-name')))

        with ZipFile("{0}.zip".format(output_zip_path), 'w') as zf:
            for matrix in matrices:
                csv_path = os.path.join(fs.location, matrix)
                df2csv(matrices[matrix], csv_path)

                zf.write(csv_path, os.path.basename(csv_path))

        with open("{0}.zip".format(output_zip_path), 'rb') as zf:
            zf_content = zf.read()

        response = HttpResponse(zf_content, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.split("{0}.zip".format(output_zip_path))[1])
    return response


def build_pair_networks(request):
    if request.method == 'POST':
        files = request.FILES.getlist('pair-csvs')

        matrices = {}

        for f in files:
            rows = [row for row in csv.reader(f, delimiter=str(u',').encode('utf-8'))]
            matrices[get_adjmat_name(f.name)] = AdjacencyMatrix(rows, events=False).build()

        fs = FileSystemStorage()
        output_zip_path = os.path.join(fs.location, clean_text(request.POST.get('pairs-output-zip-name')))

        with ZipFile("{0}.zip".format(output_zip_path), 'w') as zf:
            for matrix in matrices:
                csv_path = os.path.join(fs.location, matrix)
                df2csv(matrices[matrix], csv_path)

                zf.write(csv_path, os.path.basename(csv_path))

        with open("{0}.zip".format(output_zip_path), 'rb') as zf:
            zf_content = zf.read()

        response = HttpResponse(zf_content, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.split("{0}.zip".format(output_zip_path))[1])
    return response



