# **luatool** #

[![Join the chat at https://gitter.im/4refr0nt/luatool](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/4refr0nt/luatool?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

###Tool for loading Lua-based scripts from file to ESP8266 with nodemcu firmware

###Summary

- Allow easy uploading of any Lua-based script into the ESP8266 flash memory with [NodeMcu firmware](https://github.com/nodemcu/nodemcu-firmware)

###Other projects
Another my project for NodeMCU: ESPlorer  Integrated Development Environment (IDE) for ESP8266 developers
- [ESPlorer home page and latest binaries](http://esp8266.ru/esplorer/)
- [ESPlorer source code](https://github.com/4refr0nt/ESPlorer)

###Requirements

python 2.7, pyserial (as for esptool)

###Discuss
[http://esp8266.ru](http://esp8266.ru/forum/threads/luatool.11/)


###Changelog
v0.6.3
- fix download bug
- 
v0.6.2
- added support for nested strings
- added check to verify the UART buffer will not overflow.

v0.6.1
- put short versions of arguments back, see issue #2
- flush serial port, fixes issue #1

v0.6
- switched to argparse from getopts, renamed some arguments
- removed call-home from main.lua
- added --verbose option to show debugging
- added comments, fixed some grammar, updated README
- chmod 755'd the script so its runnable on POSIX
- checked with nodemcu 0.9.4 20141222

v0.5
- add new option  -r, --restart : auto restart module, send command "node.restart()", after file load 
- add new option  -d, --dofile  : auto run, send command "dofile('file')", after file load 
- delete line "lua script loaded by luatool" for correct line number, lines number now equal lines number in original file
- add 0.3 sec delay after write


v0.4
- now check proper answer from NodeMCU after send data.
  After send string we expect echo line, if not got it, then error message displayed "Error sending data to LuaMCU"
- if lua interpreter error received, then error message displayed "ERROR from LUA interpreter lua:..."
- add heap info and chip id to example file init.lua
- some changes in example file main.lua


###Run

####Typical use:


Edit file init.lua and set SSID and MasterPassword
Then disconnect any terminal programm, and at command prompt type

```
./luatool.py --port /dev/ttyUSB0 --src init.lua --dest init.lua --verbose

Downloader start
Set timeout 3
Set interCharTimeout 3
Stage 1. Deleting old file from flash memory
->file.remove("init.lua") -> ok
.....................................
->file.close() -> ok
--->>> All done <<<---

./luatool.py

->file.open("main.lua", "w") -> ok
->file.close() -> ok
->file.remove("main.lua") -> ok
->file.open("main.lua", "w+") -> ok
->file.writeline([[tmr.alarm(0, 1000, 1, function()]]) -> ok
->file.writeline([[if wifi.sta.getip() == nil then]]) -> ok
->file.writeline([[print("Connecting to AP...")]]) -> ok
->file.writeline([[else]]) -> ok
->file.writeline([[print('IP: ',wifi.sta.getip())]]) -> ok
->file.writeline([[tmr.stop(0)]]) -> ok
->file.writeline([[end]]) -> ok
->file.writeline([[end)]]) -> ok
->file.flush() -> ok
->file.close() -> ok
--->>> All done <<<---
```
Connect you terminal program and send command (or you can use --restart option, when loading file init.lua)
```
node.restart()
```
after reboot:
```
lua script loaded by luatool 0.4
init.lua ver 1.2
set mode=STATION (mode=1)
MAC: 	18-FE-34-98-D4-B5
chip: 	10015925
heap: 	18464
set wifi
NodeMcu 0.9.2 build 20141125  powered by Lua 5.1.4
```

send command (or you can use --dofile option, when loading file main.lua)
```
dofile("main.lua")
```
connects to your AP and displays MCU's IP address

```
> dofile("main.lua")
> IP:   192.168.1.99

```

####Examples:

```
./luatool.py --port COM4 --src file.lua --dest main.lua --baud 9600
```
- --port - COM1-COM128, default /dev/ttyUSB0
- --baud - baud rate, default 9600
- --src - source disk file, default main.lua
- --dest - destination flash file, default main.lua

If use --dest option with parameter "init.lua" - autostart init.lua after boot.
Be carefully about bugs in lua-script - may cause a boot loop. Use this option after full testing only.

Running without any parameters: load file "main.lua" via port /dev/ttyUSB0:9600 and place code into "main.lua" file into flash.

```
./luatool.py
```

after loading file to flash you can connect any terminal programm to ESP8266 and type: 
```
dofile("main.lua") 
```
for executing you lua script

If you want load and autoexecute file main.lua, command dofile("main.lua"), you can use --dofile option
```
./luatool.py --dofile
```
Typically, place wifi.setmode, wifi.sta.config commands to init.lua file for connecting to you AP with low risk of boot loop, and other code place to main.lua for manually start and debug.
