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
    ys *= -1
    transformed_data = pd.DataFrame({'x':xs, 'y':ys, 'z':zs}, index=None)
    done = False
    while not done:
        min_dist = float(input('enter the minimum distance in cm to include in the plot: '))
        max_dist = float(input('enter the maximum distance in cm to include in the plot: '))
        transformed_data = transformed_data[transformed_data.x > min_dist]
        transformed_data = transformed_data[transformed_data.x < max_dist]
        print('plot types:')
        print('0: 2D front view')
        print('1: 2D top-down view')
        print('2: 3D view')
        print('3: top-down single line view')
        mode = input('select a plot type, or "DONE" to exit: ').strip()
        if mode.upper() == 'DONE':
            done = True
        elif not mode.isnumeric():
            print('invalid input. enter a number corresponding to a plot type.')
        else:
            mode = int(mode)
            if mode == 0:
                plot_front_view(transformed_data)
            elif mode == 1:
                plot_top_view(transformed_data)
            elif mode == 2:
                plot3d(transformed_data)
            elif mode == 3:
                single_line = scan_data[scan_data.tilt == 82]
                xs, ys, zs = helpers.sph2cart(np.deg2rad(90-single_line['pan']), np.deg2rad(single_line['tilt']-82), dists)
                single_line_transformed = pd.DataFrame({'x':xs, 'y':ys, 'z':zs}, index=None)
                single_line_transformed = single_line_transformed[single_line_transformed.x > min_dist]
                single_line_transformed = single_line_transformed[single_line_transformed.x < max_dist]
                plot_top_view(single_line_transformed)
                # plot3d(single_line_transformed)

def plot_front_view(data):
    plt.scatter(-1*data.y, data.z)
    plt.axis('equal')
    # plt.title('Scanner output in 2D')
    plt.xlabel('Y (cm)')
    plt.ylabel('Z (cm)')
    plt.show()

def plot_top_view(data):
    plt.scatter(data.y, data.x)
    plt.axis('equal')
    # plt.title('Scanner output in 2D')
    plt.xlabel('y (cm)')
    plt.ylabel('x (cm)')
    plt.show()

def plot3d(data):
    ax = plt.axes(projection='3d')
    ax.scatter(data.x, data.y, data.z, marker='.', cmap='plasma')
    # Create cubic bounding box to simulate equal aspect ratio
    # from https://stackoverflow.com/a/13701747
    max_range = np.array([data.x.max()-data.x.min(), data.y.max()-data.y.min(), data.z.max()-data.z.min()]).max()
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(data.x.max()+data.x.min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(data.y.max()+data.y.min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(data.z.max()+data.z.min())
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')

    # ax.set_title('Scanner output while scanning O')
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')
    plt.show()

if __name__ == '__main__':
    main()
    