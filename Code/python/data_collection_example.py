from Scanner import Scanner
from tqdm.auto import trange

pan_start = 0
pan_end = 170
pan_interval = 10
tilt_start = 0
tilt_end = 170
tilt_interval = 10

scanner = Scanner()

data = []
print('starting data collection')
for pan in trange(pan_start, pan_end, pan_interval, desc='pan progress'):
    scanner.pan(pan)
    for tilt in trange(tilt_start, tilt_end, tilt_interval, desc='tilt progress', leave=False):
        scanner.tilt(tilt)
        scanner.delay(100)  # wait 1/10th of a second between readings to prevent shakiness
        data.append(scanner.read_sensor())

print(data)
