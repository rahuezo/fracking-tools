# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from utils.networks import NetworkComparison
from utils.matrices import AdjacencyMatrix

import csv
import re


def clean_text(s):
    return ' '.join(' '.join(re.findall(r'[a-zA-Z0-9]+', s)).split())


def network_comparison_view(request):
    context = {}
    return render(request, 'network_comparison/network_comparison.html')


def compare_networks_view(request):
    if request.method == 'POST':
        network_a_files = request.FILES.getlist('network-a-csvs')
        network_b_files = request.FILES.getlist('network-b-csvs')

        output_zip_name = clean_text(request.POST.get('output-zip-name'))

        network_a_csvs = filter(lambda x: x.name in map(lambda y: y.name, network_b_files), network_a_files)
        network_b_csvs = filter(lambda x: x.name in map(lambda y: y.name, network_a_files), network_b_files)

        for i in xrange(len(network_a_csvs)):
                rows_a = [row for row in csv.reader(network_a_csvs[i], delimiter=str(u',').encode('utf-8'))]
                rows_b = [row for row in csv.reader(network_b_csvs[i], delimiter=str(u',').encode('utf-8'))]

                network_name = network_a_csvs[i].name.split('_')[0]

                network_a = AdjacencyMatrix(rows_a).to_network()
                network_b = AdjacencyMatrix(rows_b).to_network()

                fn, header, rows = NetworkComparison(network_name, network_a, network_b).summarize()


    return redirect('network_builder:netcomp')
