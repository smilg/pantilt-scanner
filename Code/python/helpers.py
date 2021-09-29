import math
from scipy.optimize import curve_fit
from pathlib import Path
import numpy as np
import pandas as pd

def yesno_confirm(message) -> bool:
    confirm_choice = ''
    while confirm_choice not in ('y', 'n'):
        confirm_choice = input("{} (y/n) ".format(message)).lower().strip()
        if confirm_choice not in ('y', 'n'):
            print('please enter "y" or "n"')
    return confirm_choice == 'y'

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def sph2cart(az, el, r):
    rcos_theta = r * np.cos(el)
    x = rcos_theta * np.cos(az)
    y = rcos_theta * np.sin(az)
    z = r * np.sin(el)
    return x, y, z

def exp_function(x, a, b, c, d):
    return a*np.exp(b*x) + c*np.exp(d*x)

def save_csv(data):
    while True:
        data_dir = Path(input('enter a file path ending in .csv to save your data: '))
        if not data_dir.parent.is_dir():
            print('invalid path! make sure the directory exists and is accessible.')
        elif data_dir.is_file():
            if yesno_confirm('a file already exists at that location. would you like to replace it?'):
                data.to_csv(data_dir, index=False)
                break
        else:
            data.to_csv(data_dir, index=False)
            break

def load_csv():
    while True:
        data_dir = Path(input('enter a file path ending in .csv for your data: '))
        if data_dir.is_file():
            data = pd.read_csv(data_dir)
            return data
        else:
            print('the specified file was not found!')

def fit_data(data, xkey, ykey):
    popt, pcov = curve_fit(exp_function, data[xkey], data[ykey], method='trf')
    return popt