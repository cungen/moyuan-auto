from tensorflow import keras
import numpy as np
from grab_screen import grab_screen
from config import game_position, input_img_size
from game_status import person_info, battle_info
from take_action import take_action
from get_keys import key_check
import time
import matplotlib.pyplot as plt

last_screen_img = None
last_loss = 10000.0
old_p_info = {
    'blood': 1.0,
    'mana': 1.0
}
last_p_info = None


def create_move_model():
    (s_width, s_height) = input_img_size
    model = keras.models.Sequential()
    model.add(keras.layers.Input(shape=(s_width * s_height, 1), batch_size=1))
    model.add(keras.layers.LSTM(units=256, return_sequences=True))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.LSTM(units=256, return_sequences=True))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.LSTM(units=256, return_sequences=False))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.Dense(units=5, activation='softmax'))
    return model


def create_action_model():
    (s_width, s_height) = input_img_size
    model = keras.models.Sequential()
    model.add(keras.layers.Input(shape=(s_width * s_height, 1), batch_size=1))
    model.add(keras.layers.LSTM(units=256, return_sequences=True))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.LSTM(units=256, return_sequences=True))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.LSTM(units=256, return_sequences=False))
    model.add(keras.layers.Dropout(rate=0.6))
    model.add(keras.layers.Dense(units=6, activation='softmax'))
    return model


def game_loss(y_true, y_predict):
    global last_screen_img
    global last_loss
    global last_p_info
    global old_p_info

    if last_screen_img is None:
        return last_loss

    b_info = battle_info(last_screen_img)

    # 随时间损失提高
    last_loss += last_loss + 2

    # 战斗伤害收益提高，损失降低
    for damage in b_info:
        last_loss -= damage

    # 损失生命及蓝量，损失提高
    last_loss += (old_p_info.get('blood') - last_p_info.get('blood')) * 2000
    last_loss += (old_p_info.get('mana') - last_p_info.get('mana')) * 100

    return last_loss


def train():
    global last_screen_img
    global old_p_info
    global last_p_info

    move_model = create_move_model()
    action_model = create_action_model()

    move_model.compile(optimizer='adam', loss=game_loss)
    action_model.compile(optimizer='adam', loss=game_loss)

    paused = True
    r = 0
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

        if paused:
            time.sleep(1)
            continue
        elif 'Z' in keys:
            print('Exit!!')
            break

        # step 1. get screen capture
        game_img = grab_screen(game_position)
        p_info = person_info(game_img)
        print(p_info)

        # step2. check availability
        if p_info is None:
            time.sleep(1)
            continue

        # step3. get prediction and take action
        (s_width, s_height) = input_img_size
        img_small = game_img.resize(input_img_size)
        np_img_small = np.array(img_small).reshape((s_width * s_height, 1))
        if r == 0:
            move = np.random.randint(5)
            action = np.random.randint(6)
        else:
            move = move_model.predict(x=[[np_img_small]])
            action = action_model.predict(x=[[np_img_small]])
        move_index = np.argmax(move)
        action_index = np.argmax(action)
        take_action(move_index, action_index)

        # step4. get screen capture again
        last_screen_img = grab_screen(game_position)
        last_p_info = person_info(last_screen_img)

        move_model.fit([[np_img_small]], [[np.random.random(5)]])
        action_model.fit([[np_img_small]], [[np.random.random(5)]])
        old_p_info = last_p_info


if __name__ == '__main__':
    train()

