import helpers

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    print('choose calibration data:')
    calib_data = helpers.load_csv()
    print('choose scan data:')
    scan_data = helpers.load_csv()
    # fit calibration data to exponential function
    fit_params = helpers.fit_data(calib_data, 'Voltage', 'Distance')
    # convert voltages from scan data to distances in cm
    dists = helpers.exp_function(scan_data['voltage'], *fit_params)
    xs, ys, zs = helpers.sph2cart(np.deg2rad(90-scan_data['pan']), np.deg2rad(scan_data['tilt']-82), dists)
    transformed_data = pd.DataFrame({'x':xs, 'y':ys, 'z':zs}, index=None)
    transformed_data = transformed_data[transformed_data.x > 20]
    transformed_data = transformed_data[transformed_data.x < 50]
    ax = plt.axes(projection="3d")
    ax.scatter(transformed_data.x, transformed_data.y, transformed_data.z, marker='.', cmap='plasma')
    ax.set_title("Scanner output I guess :/")
    plt.show()

if __name__ == '__main__':
    main()
    