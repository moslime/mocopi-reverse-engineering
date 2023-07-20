## Common outputs
- `enter shipmode` - Printed when tracker is powered off

## Pairing
```
2000/01/01 00:00:00SYS|RTC: current GMT time is:2000-01-01 00:00:00.010 Week:6.
0000SYS|user mode
0000FLY|ft_routing_task create success
0000SYS|SW_VERSION[1.0.0.29]
nv_read_TK_cal success
0000SCR|A+G sensor id=0x24,IC is = bmi270 
 0000FLY|init read factory_module
0000BLE|BT name :QM-SS1 0B46E 
0000BAT|current_soc is 48
0000SYS|odata 50
0000SYS|odata 50
0000SYS|odata 50
0000BAT|ocv_voltage=3839,current_voltage=3824 
0000BAT|current_soc is 52
0000SYS|odata 50
0000SYS|odata 50
0000BAT|battery init success
0000BLE|sensor_ble_task_972 
0000LED|led task start !
0000SCR|sensor_init success! 
0001BAT|USB temp = 32, jeita temp = 33, jeita status = 1
0003BLE|ble connected 
 0004BLE|ble pair req 
 0006BLE|bond=1  status=0
0050BAT|ocv_voltage=3839,current_voltage=3824 
0050BAT|current_soc is 52
0100BAT|USB temp = 33, jeita temp = 34, jeita status = 1
0103POW|enter shipmode
```

## Connecting / Tracking
- `algo data` is printed around once every 2 seconds until disconnected/powered off
```
2000/01/01 00:00:00SYS|RTC: current GMT time is:2000-01-01 00:00:00.010 Week:6.
0000SYS|user mode
0000FLY|ft_routing_task create success
0000SYS|SW_VERSION[1.0.0.29]
nv_read_TK_cal success
0000FLY|init read factory_module
0000SCR|A+G sensor id=0x24,IC is = bmi270 
 0000BLE|BT name :QM-SS1 0B46E 
0000BAT|current_soc is 46
0000SYS|odata 50
0000SYS|odata 50
0000SYS|odata 50
0000BAT|ocv_voltage=3837,current_voltage=3822 
0000BAT|current_soc is 52
0000SYS|odata 50
0000SYS|odata 50
0000BAT|battery init success
0000BLE|sensor_ble_task_972 
0000LED|led task start !
0000SCR|sensor_init success! 
0001BAT|USB temp = 34, jeita temp = 35, jeita status = 1
0002BAT|USB temp = 34, jeita temp = 34, jeita status = 1
0006BLE|ble connected 
 0006FLY|ft cmd receive 18 1E FB B0 32 70 89 01 00 00 
2023/07/19 22:08:37FLY|ft cmd return 18 1E 02 18 00 00 
0838FLY|ft cmd receive 18 1E F1 B2 32 70 89 01 00 00 
0838FLY|ft cmd return 18 1E 02 18 00 00 
0838FLY|ft cmd receive 18 1F 
0838FLY|ft cmd return 18 1F 02 18 00 00 38 B3 32 70 89 01 00 00 
0838FLY|ft cmd receive 18 D6 01 
0838FLY|ft_hal_platform_task_process start task...

0838FLY|ft cmd return 18 D6 02 18 00 00 
1670 lost data[2] 
1670 lost data[5] 
0838FLY|ft cmd receive 18 1F 
0838FLY|ft cmd return 18 1F 02 18 00 00 00 1F 1F A5 41 64 73 17 
0838FLY|ft cmd receive 18 1F 
0838FLY|ft cmd return 18 1F 02 18 00 00 00 27 B3 A8 41 64 73 17 
0838FLY|ft cmd receive 18 1F 
0838FLY|ft cmd return 18 1F 02 18 00 00 00 4B 8E C0 41 64 73 17 
handle_write_req__62__len = 2 
0840SCR|TIMEOUT
0840FLY|ft cmd receive 09 02 
0840FLY|ft cmd return 09 02 02 09 00 00 32 
algo data [0] in[117] out[97]
algo data [1] in[41] out[32]
algo data [1] in[104] out[95]
algo data [1] in[40] out[30]
algo data [1] in[104] out[93]
0850BAT|USB temp = 34, jeita temp = 34, jeita status = 1
0851BAT|USB temp = 34, jeita temp = 34, jeita status = 1
0852BLE|ble disconnected
0103POW|enter shipmode
```

## Factory reset immediately after power-on
```
2000/01/01 00:00:00SYS|RTC: current GMT time is:2000-01-01 00:00:00.010 Week:6.
0000SYS|user mode
0000FLY|ft_routing_task create success
0000SYS|SW_VERSION[1.0.0.29]
nv_read_TK_cal success
0000FLY|init read factory_module
0000SCR|A+G sensor id=0x24,IC is = bmi270 
 0000BLE|BT name :QM-SS1 0B46E 
0000BAT|current_soc is 46
0000SYS|odata 50
0000SYS|odata 50
0000SYS|odata 50
0000BAT|ocv_voltage=3836,current_voltage=3821 
0000BAT|current_soc is 52
0000SYS|odata 50
0000SYS|odata 50
0000BAT|battery init success
0000BLE|sensor_ble_task_972 
0000LED|led task start !
0000SCR|sensor_init success! 
0001BAT|USB temp = 34, jeita temp = 35, jeita status = 1
0010SYS|restore_the_factory
0010POW|enter shipmode
```
