# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from utils.tag_docs_for_keywords import KeywordTagger
from utils.files import csplit, ExtensionHandler
from utils.linux_pyner import tag_document
from zipfile import ZipFile

import os
import re


def unspace(s):
    return s.strip()


def clean_text(s):
    return ' '.join(' '.join(re.findall(r'[a-zA-Z0-9]+', s)).split())


def document_tagging_view(request):
    context = {}
    return render(request, 'document_tagging/document_tagging.html', context)


def tag_documents_view(request):
    if request.method == 'POST':
        print "Form Submission"

        keywords_type = request.POST.get('keywords-type')
        documents_to_tag = request.FILES.getlist('tag-documents')

        if keywords_type == 'file':
            keywords_file = request.FILES.getlist('file-keyword-list')[0]
            keywords = map(unspace, keywords_file.read().split(','))
        else:
            manual_keyword_list = request.POST.get('manual-keyword-list')
            keywords = map(unspace, manual_keyword_list.split(','))

        fs = FileSystemStorage()
        output_zip_path = os.path.join(fs.location, clean_text(request.POST.get('output-zip-name')))

        files_to_zip = []

        for document in documents_to_tag:
            outfilename = document.name.replace(csplit(document.name)[1], '.docx')

            kt = KeywordTagger(document, keywords, os.path.join(fs.location, outfilename)).generate_output()

            if kt is not None:
                files_to_zip.append(kt)

        if files_to_zip:
            with ZipFile("{0}.zip".format(output_zip_path), 'w') as zf:
                for file_to_zip in files_to_zip:
                    path = os.path.join(fs.location, file_to_zip)
                    zf.write(path, os.path.basename(path))

            with open("{0}.zip".format(output_zip_path), 'rb') as zf:
                zf_content = zf.read()

            response = HttpResponse(zf_content, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.split("{0}.zip".format(output_zip_path))[1])
            return response
        else:
            messages.info(request, "<strong>0</strong> files were tagged because no keywords were found!")
            print "No results were found"
    return redirect('document_utilities:doctag')


def ner_tagging_view(request):
    return render(request, 'document_tagging/document_ner_tagging.html')


def tag_ner_view(request):
    if request.method == "POST":
        print "Form Submission"

        documents_to_tag = request.FILES.getlist('tag-documents')

        files_to_zip = []
        fs = FileSystemStorage()
        output_zip_path = os.path.join(fs.location, clean_text(request.POST.get('output-zip-name')))

        for document in documents_to_tag:
            content = ExtensionHandler(document).get_content()
            fname = csplit(document.name)[0] + '_tagged.txt'
            fpath = os.path.join(fs.location, fname)

            with open(fpath, 'w') as f:
                f.write(tag_document(content))

            files_to_zip.append(fpath)

        with ZipFile("{0}.zip".format(output_zip_path), 'w') as zf:
            for file_to_zip in files_to_zip:
                path = os.path.join(fs.location, file_to_zip)
                zf.write(path, os.path.basename(path))

        with open("{0}.zip".format(output_zip_path), 'rb') as zf:
            zf_content = zf.read()

        response = HttpResponse(zf_content, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            os.path.split("{0}.zip".format(output_zip_path))[1])
        return response
    return redirect('document_utilities:nertag')
