#!/usr/bin/env python
import json
import random

from PIL import Image

from predict import predict

def swap_faces(input_file, with_image=None):
    im = Image.open(input_file)
    w, h = im.width, im.height
    response = predict(input_file)

    cropped = []
    boxes = []
    for i, region in enumerate(response['outputs'][0]['data']['regions']):
        bb = region['region_info']['bounding_box']
        top = int(bb['top_row'] * h)
        bot = int(bb['bottom_row'] * h)
        left = int(bb['left_col'] * w)
        right = int(bb['right_col'] * w)
        box = (left, top, right, bot)
        boxes.append(box)
        cropped.append((im.crop(box), i))

    if with_image:
        cropped = with_image
    else:
        cropped = shuffle_cropped(cropped)
    return replace(im, boxes, cropped)

def replace(im, boxes, cropped):
    if isinstance(cropped, list):
        for box, replacer in zip(boxes, cropped):
            left, top, right, bot = box
            replacer = replacer.resize((int(right - left), int(bot - top)))
            im.paste(replacer, box)
    else:
        for box in boxes:
            left, top, right, bot = box
            im.paste(cropped.copy().resize((int(right - left), int(bot - top))), box)
    return im

def shuffle_cropped(cropped):
    all_different = False
    while not all_different:
        random.shuffle(cropped)
        all_different = True
        for i in range(len(cropped)):
            if i == cropped[i][1]:
                all_different = False
                break
    return [s[0] for s in cropped]

def transform(input_file, op):
    if op == 'swapify':
        image = None
    elif op == 'nickify':
        image = Image.open('nick-hs-zoom.jpg')
    elif op == 'smilify':
        image = Image.open('smile.png')
    elif op == 'kittify':
        image = Image.open('hellokitty.jpg')
    else:
        raise ValueError('unrecognized op: ' + op)

    return swap_faces(input_file, with_image=image)

if __name__ == '__main__':
    transform('faces.jpg', op='nickify').show()
