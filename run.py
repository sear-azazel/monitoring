from PIL import Image
import sys
import os

import pyocr
import pyocr.builders
import schedule
import time

import django
import random
import requests
import cv2
import numpy as np


sys.path.append('monitoring')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring.settings')


def job():

    if download() is False:
        return

    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    # The tools are returned in the recommended order of usage
    tool = tools[0]
    print("Will use tool '%s'" % (tool.get_name()))
    # Ex: Will use tool 'libtesseract'

    langs = tool.get_available_languages()
    print("Available languages: %s" % ", ".join(langs))
    lang = langs[0]
    print("Will use lang '%s'" % (lang))
    # Ex: Will use lang 'fra'
    # Note that languages are NOT sorted in any way. Please refer
    # to the system locale settings for the default language
    # to use.

    # no = random.randrange(20)
    # filename = 'input/image_' + str(no+1).zfill(3) + '.png'
    filename = 'input/picture.png'
    txt = tool.image_to_string(
        Image.open(filename),
        lang=lang,
        builder=pyocr.builders.TextBuilder(tesseract_layout=3)
    )
    django.setup()
    from datas.models import Recognition

    result = 0
    txt = txt.replace('/', '7')
    if (is_int(txt)):
        result = int(txt)
    Recognition.objects.create(recognition_text=result)
    print(txt)


def download():
    url = 'http://192.168.150.110:8000/static/source/picture.jpg'
    try:
        print('download start.')
        r = requests.get(url, timeout=(5, 10))
        name = 'input/tmp.jpg'
        with open(name, mode='wb') as f:
            f.write(r.content)

        print('read start.')
        im = cv2.imread(name, 0)
        # img[top : bottom, left : right]
        print('cut start.')
        dst = im[170:300, 200:420]
        print('resize start.')
        dst2 = cv2.resize(dst, None, fx = 4, fy = 4)
        print('threshold start.')
        ret, thresh = cv2.threshold(dst2, 127, 255, cv2.THRESH_BINARY)
        print('ones start.')
        kernel = np.ones((5, 5), np.uint8)
        print('dilate start.')
        dilation = cv2.dilate(thresh, kernel, iterations = 0)

        # orgHeight, orgWidth = dst.shape[:2]
        # size = (orgHeight*2, orgWidth*2)
        out = dilation

        cv2.imwrite('input/picture.png', out)

        return True

    except Exception as err:
        print(err)
        return False


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def exec_schedule():

    # 1分毎にjobを実行
    schedule.every(1).minutes.do(job)
    # 5秒毎にjobを実行
    # schedule.every(1).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    job()
    exec_schedule()
