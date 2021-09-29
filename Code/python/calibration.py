from Scanner import Scanner
import helpers
from pathlib import Path
import numpy as np
import pandas as pd
import scipy.optimize
import matplotlib.pyplot as plt


def collect_data():
    s = Scanner()
    print('centering scanner...')
    s.center()
    print('done!')
    dists = []
    voltages = []

    print('beginning calibration routine...')
    done = False
    while not done:
        dist = input('enter the current distance in cm, or "DONE" to exit: ').strip()
        if dist.upper() == 'DONE':
            done = True
        elif dist.isnumeric():
            dist = int(dist)
            if dist < 20:
                print('the sensor is unreliable at distances below 20 cm, place it further away.')
            elif dist > 150:
                print('the sensor is unreliable at distances greater than 150 cm, place it closer.')
            else:
                dists.append(dist)
                v = s.read_sensor()[2]
                print('voltage at {}cm = {}'.format(dist, v))
                voltages.append(v)

        else:
            print('invalid input!')
    
    data = pd.DataFrame({'Distance': dists, 'Voltage': voltages}, index=None)
    helpers.save_csv(data)


def plot_data():
    data = helpers.load_csv()
    data.plot('Distance', 'Voltage')
    fit_dist = np.linspace(20, 150, 100)
    params = helpers.fit_data(data, 'Distance', 'Voltage')
    fit_volt = helpers.exp_function(fit_dist, *params)
    plt.plot(fit_dist, fit_volt)
    plt.show()


def verify_calibration():
    print('select a calibration dataset')
    calib_data = helpers.load_csv()
    print('select a dataset to compare to the calibration dataset (generate using calibrate function)')
    test_data = helpers.load_csv()
    # fit calibration data to exponential function
    fit_params = helpers.fit_data(calib_data, 'Voltage', 'Distance')

    predicted_dists = helpers.exp_function(test_data['Voltage'], *fit_params)
    print(predicted_dists)
    actual_dists = test_data['Distance']
    error = (np.abs(actual_dists-predicted_dists)/predicted_dists)*100

    plt.plot(actual_dists, error)
    plt.xlabel('Actual Distance (cm)')
    plt.ylabel('Percent error')
    plt.show()


def main():
    done = False
    while not done:
        print('calibration functions:')
        print('0: collect calibration data')
        print('1: plot calibration data')
        print('2: verify calibration')
        mode = input('select a calibration function, or "DONE" to exit: ').strip()
        if mode.upper() == 'DONE':
            done = True
        elif not mode.isnumeric():
            print('invalid input. enter a number corresponding to a function.')
        else:
            mode = int(mode)
            if mode == 0:
                collect_data()
            elif mode == 1:
                plot_data()
            elif mode == 2:
                verify_calibration()


if __name__ == '__main__':
    main()