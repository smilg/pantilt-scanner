# this is most likely no longer useful, but i don't want to get rid of it yet

import matplotlib.pyplot as plt
import math
import serial
from numpy import mean
from tqdm.auto import trange

from Scanner import Scanner

pan_start = 0
pan_end = 170
pan_interval = 1
tilt_start = 0
tilt_end = 170
tilt_interval = 1

delay_interval = 100 # ms

def scan(s):
    xs, ys, ds = [], [], []
    direction = 1
   
    # Starting from (0,0), not center (85,85), if that ever matters
    for tilt_pos in trange(tilt_start, tilt_end, tilt_interval, desc="tilt progress"):
        s.tilt(tilt_pos)
        s.delay(100)
        for pan_pos in trange(pan_start, pan_end, pan_interval, desc="pan progress"):
            pan_pos *= direction
            s.pan(pan_pos)
            s.delay(100)
            dist = s.read_sensor()
            xs.append(dist*math.sin(pan_pos))
            ys.append(dist*math.sin(tilt_pos))
            ds.append(dist)
        direction *= -1
    
    threshold = mean(ds)
    # MVP: either there's an object here or there's not :)
    zs = [(1 if d > threshold else 0) for d in ds]
    return (xs, ys, zs)

def visualize(xs, ys, zs):
    ax = plt.axes(projection="3d")
    # Do we want a surface...? Scatter plot may be ugly
    ax.scatter(xs, ys, zs, marker='x')
    ax.set_title("Scanner output I guess :/")
    plt.show()

def main():
    s = Scanner()
    xs, ys, zs = scan(s)
    visualize(xs, ys, zs)

if __name__ == "__main__":
    main()
