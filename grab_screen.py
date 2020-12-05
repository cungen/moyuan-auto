# In[0]
import numpy as np
import win32gui
import win32con
import win32api
import pyscreenshot as sc
import matplotlib.pyplot as plt


#%%
def grab_screen(region=None):
    if region:
        left, top, width, height = region
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    img = sc.grab(bbox=(left, top, left + width, top + height)).convert('L')

    return img
