from tensorflow import keras
import numpy as np
from grab_screen import grab_screen
from config import game_position, input_img_size
from game_status import person_info, battle_info
from PIL import Image
from take_action import take_action
from get_keys import key_check
import time

last_screen_img = None
last_loss = 10000.0

# percent
last_p_info = {
    'blood': 1.0,
    'mana': 1.0
}


def create_move_model():
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


def create_action_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Input(shape=(14400, 1), batch_size=1))
    model.add(keras.layers.LSTM(units=256, return_sequences=True))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.LSTM(units=256, return_sequences=True))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.LSTM(units=256, return_sequences=False))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.Dense(units=6, activation='softmax'))
    return model


def game_loss():
    p_info = person_info(last_screen_img)
    b_info = battle_info(last_screen_img)
    global last_loss
    # 随时间损失提高
    last_loss += last_loss + 2

    # 战斗伤害收益提高，损失降低
    for damage in b_info:
        last_loss -= damage

    # 损失生命及蓝量，损失提高
    last_loss += (last_p_info.get('blood') - p_info.get('blood')) * 2000
    last_loss += (last_p_info.get('mana') - p_info.get('mana')) * 100

    return last_loss


def train():
    move_model = create_move_model()
    action_model = create_action_model()

    # move_model.compile(optimizer='adam', loss=game_loss)
    # action_model.compile(optimizer='adam', loss=game_loss)

    paused = True
    while True:
        keys = key_check()
        if 'return' in keys:
            if paused:
                paused = False
                print('Started !!!')
                time.sleep(1)
            else:
                paused = True
                print('Stopped !!!')
                time.sleep(1)
            continue
        if not paused and keys:
            if 'Z' in keys:
                print('Exit!!')
                break


if __name__ == '__main__':
    # grab screen
    # img = grab_screen(game_position)
    # img = Image.open('images/test_multi.png').convert('L')
    # img_small = img.resize(input_img_size)
    # np_img_small = np.array(img_small).reshape((14400, 1))
    # print(np_img_small.size)
    # print(np_img_small.shape)
    train()

