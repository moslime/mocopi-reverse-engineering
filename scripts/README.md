# Scripts

## These scripts all assume you're running on linux with the `bluepy` and `scipy` python modules installed.
To connect your tracker, just pair it like any other bluetooth device using your distro's bluetooth manager or `bluetoothctl`. You may need to restart bluetooth or the tracker itself to connect after pairing.

### `mocopi-to-slime-POC.py` - Early prototype for getting Mocopi data into SlimeVR
This is a very early prototype of the software that will send Mocopi data to slime. Something about the rotation of the tracker isn't correct so calibration doesn't work correctly and it's not actually usable yet.\
Edit these settings in the file before use:\
`tracker_addr` - Put the MAC address of your tracker here\
`UDP_IP` - Set this to the IP that the SlimeVR server is running on

### `read-sensor.py` - Prints the raw data from the sensor as unsigned integers
Edit these settings in the file before use:\
`tracker_addr` - Put the MAC address of your tracker here\
`formatted` - Whether or not you want to view each byte seperately

### `visualize.py` - Decodes the data and sends it over to a quaternion visualizer
Relies on `pyteapot.py` from [this repo](https://github.com/thecountoftuscany/PyTeapot-Quaternion-Euler-cube-rotation). That file is included here just in case something happens to the original.\
Edit these settings before use:\
`pyteapot.py` - Change `useQuat` to true, if not already set\
`visualize.py` - Ensure `tracker_addr` is set to your tracker MAC address and ensure `UDP_PORT` matches the one set in `pyteapot.py`. If you want to print the quaternion values to the terminal, set `debug` to true
