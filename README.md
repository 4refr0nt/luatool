# **luatool** #

###Tool for loading lua-based script from file to ESP8266 with nodemcu firmware
version 0.2

#Summary

- allow easy load any lua-based script into ESP8266 with [NodeMcu firmware](https://github.com/nodemcu/nodemcu-firmware)

#Requirements

python 2.7, pyserial (as for esptool)

#Run

####Examples:

```
./luatool -p COM4 -f file.lua -t main.lua -b 9600
```
- -p --port - COM1-COM128, default COM3
- -b --baud - baud rate, default 9600
- -f --file file to load, default init.lua
- -t --to - flash file name, default main.lua
if you use -t option with parameter "init.lua" - autostart init.lua after boot
Be carefully about bug's in lua-script - may be boot loop. Use this option after full testing only.

Running without any parameters: load file "main.lua" via port COM3:9600 and place code into "main.lua" file into flash.

```
./luatool
```

after loading file to flash you can connect any terminal programm to ESP8266 and type: 
```
dofile("main.lua") 
```
for executing you lua script

Typically, place wifi.setmode, wifi.sta.config commands to init.lua file for connecting to you AP with low risk of boot loop, and other code place to main.lua for manually start and debug.
