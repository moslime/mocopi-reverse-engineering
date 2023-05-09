# mocopi-reverse-engineering
Reverse engineering the mocopi trackers, with the eventual goal of streaming the data to SlimeVR, forgoing the need for a phone and the mocopi app

# General Info
BLE SoC - https://www.renesas.com/us/en/products/wireless-connectivity/bluetooth-low-energy/da14683-smartbond-bluetooth-low-energy-50-soc-enhanced-security \
(found by searching one of the BLE service UUIDs which linked me [here](http://bbs.eeworld.com.cn/thread-822943-1-1.html)

IMUs (unsure if one or both are present) - [BMI270](https://www.bosch-sensortec.com/media/boschsensortec/downloads/product_flyer/bst-bmi270-fl000.pdf), [ICM40608](https://static6.arrow.com/aropdfconversion/c4a55e5ba65360490f9914c80186aa28bc5c3857/icm-40608.pdf)\
(Found by running strings on a firmware update embedded in app)


# Reading data
Right now any scripts uploaded here assume you're running on linux. 

read-sensors.py - Needs bluepy installed using pip. To use, just pair your tracker like any other bluetooth device (you may need to toggle bluetooth or restart the tracker afterwards), edit the file and put your tracker MAC address then run it. If data doesn't start coming out after a few seconds just restart the script.
