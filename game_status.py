# -*- coding: utf-8 -*-
"""game status

get game status
"""
from PIL import Image
import matplotlib.pyplot as plt
import easyocr as ocr
import re


def person_info(image):
    """
    :param image: PIL instance
    :return: dict
    """
    blood_field = image[60:90, 130:380]
    mana_field = image[100:122, 350:425]
    reader = ocr.Reader(['en'])
    try:
        (p, blood_text, ac) = reader.readtext(blood_field)[0]
        (p, mana_text, ac) = reader.readtext(mana_field)[0]

        [blood_now, blood_max] = re.split(r'\W+', blood_text)
        [mana_now, mana_max] = re.split(r'\W+', mana_text)

        return {
            'blood': blood_now / blood_max,
            'mana': mana_now / mana_max
        }
    except:
        print('no mana and blood info')
        return None


def battle_info(image):
    """
    :return: dict info of battle
    """
    battle_field = image[250:650, 400:1150]
    reader = ocr.Reader(['en'])
    try:
        battle_text = reader.readtext(battle_field, allowlist='0123456789')
        rs = []
        for item in battle_text:
            try:
                rs.append(int(item[1]))
            except ValueError:
                print('not recognise number ', item[1])
        return rs
    except:
        print('no battle info')
        return None

