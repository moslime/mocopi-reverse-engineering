# mocopi-reverse-engineering
Reverse engineering the mocopi trackers, with the eventual goal of streaming the data to SlimeVR, forgoing the need for a phone and the mocopi app\
If you want to play around with the data, head over to the `scripts` folder and check out the examples there.

## Go check out [moslime](https://github.com/lmore377/moslime)! It's the project that this repo was created for in the first place.

## Disclaimer
Mocopi is a trademark owned by Sony. None of this is endorsed by Sony, nor are they affiliated with the people associated with this repository. All info in this repository is provided as is, without warranty. Nothing here should cause damage to your trackers; however, only use the info in this repository if you agree to assume the risks therein.

## General Info
- The batteries in the trackers last around 18 hours and charge from 0-100 in around 50mins.
- At a hardware level (probably firmware too) the sensors are all identical. The only difference is the colored plastic circle and the app will even let you assign a tracker to a different body part.
- The sensors can be factory reset by quickly pressing the button 10-15 times (or until it blinks red and blue)
- The sensors zero out their axes when the command to start the data stream is sent. It takes about a second to zero before the data starts streaming.
- The mocopi app has lots of hardcoded time constraints and makes very heavy use of System.currentTimeMillis, which is not suitable for real-time applications. This points to the app itself being the culprit for the widespread drift problem (thx PlatinumVR for that tip). At a hardware level, the IMU being used seems to be very resistant to drift as the only thing that was causing it to visibly drift was very fast/sudden movements and hard impacts.
- The sensors don't seem to be impacted at all by magnetic interference, disproving the theory that the drift comes from the mounting mechanism. A video of this can be found in the `resources` folder.
- The default Bluetooth LE MTU is 20 bytes and the sensor sends 36 at a time. Make sure you set the MTU to 36 or greater in whatever you're using to get sensor data.

## Hardware Info
BLE SoC - Might be the [DA14683](https://www.renesas.com/us/en/products/wireless-connectivity/bluetooth-low-energy/da14683-smartbond-bluetooth-low-energy-50-soc-enhanced-security) \
(Found by searching one of the BLE service UUIDs which led me [here](http://bbs.eeworld.com.cn/thread-822943-1-1.html)

IMUs (unsure if one or both are present) - [BMI270](https://www.bosch-sensortec.com/media/boschsensortec/downloads/product_flyer/bst-bmi270-fl000.pdf), [ICM40608](https://static6.arrow.com/aropdfconversion/c4a55e5ba65360490f9914c80186aa28bc5c3857/icm-40608.pdf)\
(Found by running strings on a firmware update embedded in the app)


## Updating / OTA info
- The mocopi app uses the [SmartBond™ SUOTA](https://lpccs-docs.renesas.com/Tutorial_SDK6/suota_overview.html) protocol to update the trackers. If you extract the firmware from the mocopi app (filename: SI6285A_dev.img) you can use the [Renesas SUOTA](https://play.google.com/store/apps/details?id=com.dialog.suota) app to update the trackers manually. If you do this, don't mess with the default Parameter settings as editing them can permanently damage your tracker. Firmware files will not be provided because they can easily be extracted from the mocopi app and if you can do that you can understand the risks that come with doing an update like this.

## Credits
Huge thanks to [@PlatinumVsReality](https://github.com/PlatinumVsReality) for reaching out and helping me get this all going.
