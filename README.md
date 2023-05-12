# mocopi-reverse-engineering
Reverse engineering the mocopi trackers, with the eventual goal of streaming the data to SlimeVR, forgoing the need for a phone and the mocopi app


## General Info
- The sensors can be factory reset by quickly pressing the button 10-15 times (or until it blinks red and blue)
- The sensors self-calibrate when the command to start the data stream is sent. It takes about a second to calibrate before the data starts streaming.
- The mocopi app has lots of hardcoded time constraints and makes very heavy use of System.currentTimeMillis, which is not suitable for real-time applications. This points to the app itself being the culprit for the widespread drift problem (thx PlatinumVR for that tip). At a hardware level, the IMU being used seems to be very resistant to drift as the only thing that was causing it to visibly drift was very fast/sudden movements and hard impacts.
- The sensors don't seem to be impacted at all by magnetic interference, disproving the theory that the drift comes from the mounting mechanism. A video of this can be found in the `resources` folder.

## Hardware Info
BLE SoC - Might be the [DA14683](https://www.renesas.com/us/en/products/wireless-connectivity/bluetooth-low-energy/da14683-smartbond-bluetooth-low-energy-50-soc-enhanced-security) \
(Found by searching one of the BLE service UUIDs which led me [here](http://bbs.eeworld.com.cn/thread-822943-1-1.html)

IMUs (unsure if one or both are present) - [BMI270](https://www.bosch-sensortec.com/media/boschsensortec/downloads/product_flyer/bst-bmi270-fl000.pdf), [ICM40608](https://static6.arrow.com/aropdfconversion/c4a55e5ba65360490f9914c80186aa28bc5c3857/icm-40608.pdf)\
(Found by running strings on a firmware update embedded in the app)
