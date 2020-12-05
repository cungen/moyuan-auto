#%%
from get_keys import key_check
import time



paused = False
while True:
    keys = key_check()
    if 'P' in keys:
        if paused:
            paused = False
            print('unpaused!')
            time.sleep(1)
        else:
            paused = True
            print('Pausing!')
            time.sleep(1)

        continue

    if 'O' in keys:
        print('Stopped')
        break

    if not paused and keys:
        print(keys)
# %%

