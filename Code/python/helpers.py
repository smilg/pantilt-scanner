from scipy.optimize import curve_fit
from pathlib import Path
import numpy as np
import pandas as pd

def yesno_confirm(message: str) -> bool:
    '''
    confirm a yes or no command line input option with the user.

    Args:
        message (str): the question to ask the user.

    Returns:
        bool: True if the user answers "y", False if not.
    '''
    confirm_choice = ''
    while confirm_choice not in ('y', 'n'):
        confirm_choice = input("{} (y/n) ".format(message)).lower().strip()
        if confirm_choice not in ('y', 'n'):
            print('please enter "y" or "n"')
    return confirm_choice == 'y'

def map(x, in_min, in_max, out_min, out_max):
    '''
    maps a value from one range to another.

    Args:
        x: the value to be mapped
        in_min: the minimum range to map the value from
        in_max: the maximum range to map the value from
        out_min: the minimum range to map the value to
        out_max: the maximum range to map the value to

    Returns:
        the new value, mapped from one range to the other.
    '''
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def sph2cart(az, el, r):
    '''
    transforms a point from spherical coordinates to cartesian coordinates.

    Args:
        az: azimuth - pan angle
        el: elevation - tilt angle
        r: radius - distance

    Returns:
        x, y, and z cartesian coordinates.
    '''
    rcos_theta = r * np.cos(el)
    x = rcos_theta * np.cos(az)
    y = rcos_theta * np.sin(az)
    z = r * np.sin(el)
    return x, y, z

def exp_function(x, a, b, c, d):
    '''
    used to provide a function to fit the calibration curve to.
    '''
    return a*np.exp(b*x) + c*np.exp(d*x)

def save_csv(data):
    '''
    prompts the user to save a DataFrame as a csv file

    Args:
        data (DataFrame): the data to save as a csv
    '''
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
    '''
    prompts the user to load data from a csv into a DataFrame

    Returns:
        DataFrame: data constructed from the selected csv file
    '''
    while True:
        data_dir = Path(input('enter a file path ending in .csv for your data: '))
        if data_dir.is_file():
            data = pd.read_csv(data_dir)
            return data
        else:
            print('the specified file was not found!')

def fit_data(data, xkey, ykey):
    '''
    fits data to a curve function and returns the constants found through doing so.

    Args:
        data (DataFrame): the data to be fit
        xkey (str): the key of the x axis to fit
        ykey (str): the key of the y axis to fit

    Returns:
        a list of constants from the equation. 
    '''
    popt, pcov = curve_fit(exp_function, data[xkey], data[ykey], method='trf')
    return popt