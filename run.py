from PIL import Image
import sys
import os

import pyocr
import pyocr.builders
import schedule
import time

import django
import random


sys.path.append('monitoring')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring.settings')


def job():

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

    no = random.randrange(20)
    filename = 'input/image_' + str(no+1).zfill(3) + '.png'
    txt = tool.image_to_string(
        Image.open(filename),
        lang="jpn",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    django.setup()
    from datas.models import Recognition
    Recognition.objects.create(recognition_text=txt)
    print(txt)


def exec_schedule():

    # 1分毎にjobを実行
    schedule.every(1).minutes.do(job)
    # 5秒毎にjobを実行
    # schedule.every(1).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    exec_schedule()
