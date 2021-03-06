from Scanner import Scanner
import helpers

from numpy import mean
import pandas as pd
from tqdm.auto import trange

pan_interval = 1
tilt_interval = 1
pan_center = 90     # determined experimentally
tilt_center = 82    # determined experimentally
pan_radius = 24     # set based on how wide the thing being scanned is
tilt_radius = 35    # set based on how tall the thing being scanned is 

def scan(s):
    xs, ys, ds = [], [], []
    print('starting scan')
    s.delay(1000)
    for pan_pos in trange(pan_center-pan_radius, pan_center+pan_radius,
                                pan_interval, desc="pan progress"):
        s.pan(pan_pos)
        for tilt_pos in trange(tilt_center-tilt_radius, tilt_center+tilt_radius,
                            tilt_interval, desc="tilt progress", leave=False):
            s.tilt(tilt_pos)
            dist = s.read_sensor()
            xs.append(dist[0])
            ys.append(dist[1])
            ds.append(dist[2])
    
    return pd.DataFrame({'pan': xs, 'tilt': ys, 'voltage': ds})

def main():
    s = Scanner()
    data = scan(s)
    helpers.save_csv(data)

if __name__ == "__main__":
    main()
