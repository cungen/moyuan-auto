# -*- coding: utf-8 -*-
"""game status

get game status
"""
import numpy as np
import easyocr as ocr
import re

reader = ocr.Reader(['en'], gpu=False)


def person_info(img):
    """
    :param img: PIL instance
    :return: dict
    """
    global reader
    image = np.array(img)
    blood_field = image[60:90, 130:380]
    mana_field = image[100:122, 350:425]

    try:
        (p, blood_text, ac) = reader.readtext(blood_field)[0]
        (p, mana_text, ac) = reader.readtext(mana_field)[0]

        [blood_now, blood_max] = re.split(r'\W+', blood_text)
        [mana_now, mana_max] = re.split(r'\W+', mana_text)

        return {
            'blood': float(blood_now) / float(blood_max),
            'mana': float(mana_now) / float(mana_max)
        }
    except:
        print('no mana and blood info')
        return None


def battle_info(img):
    """
    :return: dict info of battle
    """
    global reader
    image = np.array(img)
    battle_field = image[250:650, 400:1150]
    try:
        battle_text = reader.readtext(battle_field, allowlist='0123456789')
        rs = []
        for item in battle_text:
            try:
                rs.append(float(item[1]))
            except ValueError:
                print('not recognise number ', item[1])
        return rs
    except:
        print('no battle info')
        return []

