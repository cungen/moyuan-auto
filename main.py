#%%
from tensorflow import keras
import numpy as np
from grab_screen import grab_screen
from config import game_position, input_img_size
from game_status import person_info, battle_info
from PIL import Image
import matplotlib.pyplot as plt
import easyocr as ocr

last_screen_img = None
last_score = 2000
last_p_info = {
    'blood': 1000,
    'mana': 100
}


def create_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Input(shape=(14400, 1), batch_size=1))
    model.add(keras.layers.LSTM(units=256, return_sequences=True))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.LSTM(units=256, return_sequences=True))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.LSTM(units=256, return_sequences=False))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.Dense(units=5, activation='softmax'))
    return model


def game_loss(y_true, y_predict):
    p_info = person_info(last_screen_img)
    b_info = battle_info(last_screen_img)
    global last_score
    # 随时间损失提高
    last_score += last_score + 2

    # 战斗伤害收益提高
    for damage in b_info:
        last_score -= damage

    # 损失生命及蓝量，损失提高
    return last_score


def train():
    train_model = create_model()
    train_model.compile(optimizer='adam', loss=game_loss)


if __name__ == '__main__':
    # grab screen
    # img = grab_screen(game_position)
    img = Image.open('images/test_multi.png').convert('L')
    img_small = img.resize(input_img_size)
    np_img_small = np.array(img_small).reshape((14400, 1))
    print(np_img_small.size)
    print(np_img_small.shape)


# %%
