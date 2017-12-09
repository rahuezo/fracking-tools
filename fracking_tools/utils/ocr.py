import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from files import csplit, create_tmp_dir, empty_trash

import multiprocessing as mp
import os
import pytesseract
import time

try:
    from PIL import Image
except:
    import Image


def ocr_name(f):
    wd = os.path.split(f)[0]
    fn = csplit(os.path.split(f)[1])[0] + '.txt'
    return os.path.join(wd, fn)


def to_txt(content, f):
    with open(f, 'w') as txtfile:
        txtfile.write(content)


def pdf2img(f):
    tmp_dir = create_tmp_dir(f)
    print "\nConverting {0} to images...".format(f)
    out_path = os.path.join(tmp_dir, "file-%03d.png")
    gs_command = r'gs -sDEVICE=pnggray -o "{0}" -r300 "{1}"'.format(out_path, f)
    os.popen(gs_command)
    print "\tCreated {0} images!".format(len(os.listdir(tmp_dir)))
    return tmp_dir, ocr_name(f)


def tess_img2string(img_file, i):
    content = ''
    current_img = Image.open(img_file)
    content += pytesseract.image_to_string(current_img)
    if i > 0:
        content += '\n{0}\n'.format('-' * 50)
    return content


def img2txt(tmp_dir, ocr_fn, clean=True):
    print "\nConverting images to txt..."
    files = sorted(map(lambda x: os.path.join(tmp_dir, x), os.listdir(tmp_dir)))
    pool = mp.Pool(processes=mp.cpu_count()*4)
    results = [pool.apply_async(tess_img2string, (img_file, i, )) for i, img_file in enumerate(files)]
    content = ' '.join([r.get() for r in results])
    print "\tCreated {0}!".format(ocr_fn)
    if clean:
        empty_trash(tmp_dir)
    return content


def apply_ocr(f, as_file=False):
    start = time.time()

    tmp_dir, ocr_fn = pdf2img(f)

    content = img2txt(tmp_dir, ocr_fn, clean=True)

    if not as_file:
        print "OCR'ed in {0}s".format(round(time.time() - start, 2))
        return content

    to_txt(content, ocr_fn)
    msg = "\nOCR'ed {0} in {1}s".format(os.path.split(f)[1], round(time.time() - start, 2))

    print msg


# apply_ocr('/mnt/c/Users/Rudy/Downloads/Town of New Hartford 2012_ocr.pdf', as_file=True)
