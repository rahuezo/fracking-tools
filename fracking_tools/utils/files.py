from docx import Document

import PyPDF2
import shutil
import re
import os


def csplit(f):
    if f.count('.') == 1:
        return f.split('.')[0], '.' + f.split('.')[1]
    elif f.count('.') > 1:
        period = [i for i in xrange(len(f)) if f[i] == '.'][-1]
        return f[:period], f[period:]
    else:
        return None


def get_text(s):
    return ' '.join(' '.join(re.findall(r'[ -~]+', s)).split())


def valid_extension(f, ext_list):
    if csplit(f):
        return any(csplit(f)[1].lower() == e.lower() for e in ext_list)
    else:
        return False


def is_scanned(f):
    with open(f, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        return len(get_text(' '.join([pdf_reader.getPage(p).extractText() for p in xrange(pdf_reader.numPages)]))) == 0


def read_docx(f):
    document = Document(f)
    return get_text(' '.join([p.text.encode('ascii', errors='ignore') for p in document.paragraphs]))


def read_pdf(f):
    if not is_scanned(f):
        pdf_reader = PyPDF2.PdfFileReader(f)
        return get_text(' '.join([pdf_reader.getPage(p).extractText()
                                  for p in xrange(pdf_reader.numPages)]).encode('ascii', errors='ignore'))
    else:
        pass
        # from ocr import apply_ocr
        # return get_text(apply_ocr(f).encode('ascii', errors='ignore'))


def read_txt(f):
    try:
        return get_text(f.read())
    except:
        with open(f, 'r') as in_file:
            return in_file.read()


def create_tmp_dir(f):
    print "\nCreating temporary directory...\n"
    wd = os.path.split(f)[0]
    fname = os.path.split(f)[1].split('.')[0] + '_tmp'
    tmp_dir_path = os.path.join(wd, fname)

    if not os.path.exists(tmp_dir_path):
        os.mkdir(tmp_dir_path)
    else:
        print "Directory exists! Removing old one first."
        shutil.rmtree(tmp_dir_path)
        os.mkdir(tmp_dir_path)
    print "\tCreated {0}!".format(tmp_dir_path)
    return tmp_dir_path


def empty_trash(d):
    print "Removing {0}...".format(d)
    shutil.rmtree(d)
    print "\tRemoved {0}!".format(d)


class ExtensionHandler:
    def __init__(self, f):
        self.f = f
        try:
            self.extension = csplit(self.f.name)[1].lower()
        except:
            self.extension = csplit(self.f)[1].lower()

    def get_content(self):
        if self.extension == '.pdf':
            return read_pdf(self.f)
        elif self.extension == '.docx':
            return read_docx(self.f)
        elif self.extension == '.txt':
            return read_txt(self.f)
        else:
            raise Exception("{ext}: This file extension is not supported!".format(ext=self.extension))

