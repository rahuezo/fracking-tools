# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from zipfile import ZipFile
from utils.networks import NetworkComparison, to_csv
from utils.matrices import AdjacencyMatrix
from django.http import HttpResponse

import csv
import re
import os


def clean_text(s):
    return ' '.join(' '.join(re.findall(r'[a-zA-Z0-9]+', s)).split())


def network_comparison_view(request):
    context = {}
    return render(request, 'network_comparison/network_comparison.html')


def compare_networks_view(request):
    if request.method == 'POST':
        network_a_files = request.FILES.getlist('network-a-csvs')
        network_b_files = request.FILES.getlist('network-b-csvs')

        network_a_label = request.POST.get('net-a-label')
        network_b_label = request.POST.get('net-b-label')

        network_a_csvs = filter(lambda x: x.name in map(lambda y: y.name, network_b_files), network_a_files)
        network_b_csvs = filter(lambda x: x.name in map(lambda y: y.name, network_a_files), network_b_files)

        print network_a_label, network_b_label
        comparisons = {}

        for i in xrange(len(network_a_csvs)):
                rows_a = [row for row in csv.reader(network_a_csvs[i], delimiter=str(u',').encode('utf-8'))]
                rows_b = [row for row in csv.reader(network_b_csvs[i], delimiter=str(u',').encode('utf-8'))]

                network_name = network_a_csvs[i].name.split('_')[0]

                network_a = AdjacencyMatrix(rows_a).to_network()
                network_b = AdjacencyMatrix(rows_b).to_network()

                fn, header, rows = NetworkComparison(network_name, network_a, network_b,
                                                     network_a_label, network_b_label).summarize()

                comparisons[fn] = [header, rows]

        fs = FileSystemStorage()
        output_zip_path = os.path.join(fs.location, clean_text(request.POST.get('output-zip-name')))

        with ZipFile("{0}.zip".format(output_zip_path), 'w') as zf:
            for comparison in comparisons:
                csv_path = os.path.join(fs.location, comparison)

                to_csv(csv_path, comparisons[comparison][0], comparisons[comparison][1])
                zf.write(csv_path, os.path.basename(csv_path))

        with open("{0}.zip".format(output_zip_path), 'rb') as zf:
            zf_content = zf.read()

        response = HttpResponse(zf_content, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.split("{0}.zip".format(output_zip_path))[1])

        return response
    return redirect('network_builder:netcomp')
