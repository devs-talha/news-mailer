import datetime
import pytz
import requests
from PIL import Image
import io
import re
import os


def download_images(images): 
    for image in images:
        downloaded_image = requests.get(image['url'])
        image['data'] = downloaded_image.content
        compress_image(image)

def compress_image(image):
    compressed_buffer = io.BytesIO()
    with Image.open(io.BytesIO(image['data'])) as img:
        img.save(compressed_buffer, format='JPEG', optimize=True, quality=int(os.getenv("IMAGE_QUALITY", "10")))
    image['data'] = compressed_buffer.getvalue()
   
def parse_date(date):
        start_index = date.index('2')
        return date[start_index:start_index + 10]    

def verify_todays_date(date):
    GMT = int(os.getenv('GMT', '5'))
    return date == get_gmt_date(GMT)

def get_gmt_date(gmt_offset):
    gmt_timezone = pytz.timezone(f'Etc/GMT{-gmt_offset if gmt_offset >= 0 else "+" + str(abs(gmt_offset))}')
    return str(datetime.datetime.now(gmt_timezone).date())

def invert_date(date, split_delimiter="-", join_delimiter="-"):
    split = date.split(split_delimiter)
    split[0], split[2] = split[2], split[0]
    return join_delimiter.join(split)

def second_last_occurrence_index(input_string, target_char):
    last_index = input_string.rfind(target_char)
    if last_index == -1:
        return -1
    second_last_index = input_string.rfind(target_char, 0, last_index)
    return second_last_index

def sanitize_name(name):
    # Characters not allowed in filenames across Linux, macOS, and Windows
    forbidden_chars = r'[\\/*?:"<>|]'
    # Replace forbidden characters with dash
    sanitized_name = re.sub(forbidden_chars, '-', name)
    return sanitized_name

def split_into_sections(images):
    images_dict = {}

    for image in images:
        if image['section'] in images_dict:
            images_dict[image['section']].append(image)
        else:
            images_dict[image['section']] = [image]
    
    for value in images_dict.values():
        value.sort(key=lambda x: x['name'])

    return images_dict

def split_str(string: str, delimiter=","):
    split = string.split(delimiter)
    for section in split:
        section = section.strip()
    return split