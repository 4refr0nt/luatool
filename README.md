# **luatool** #

###Tool for loading lua-based script from file to ESP8266 with nodemcu firmware

###Summary

- allow easy load any lua-based script into ESP8266 flash memory with [NodeMcu firmware](https://github.com/nodemcu/nodemcu-firmware)

###Requirements

python 2.7, pyserial (as for esptool)

###Discuss
[http://esp8266.ru](http://esp8266.ru/forum/threads/luatool.11/)


###Changelog

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
./luatool -p COM4 -f init.lua -t init.lua 

Downloader start
Set timeout 3
Set interCharTimeout 3
Stage 1. Deleting old file from flash memory
->file.remove("init.lua") -> ok
.....................................
->file.close() -> ok
--->>> All down <<<---

./luatool 

Downloader start
Set timeout 3
Set interCharTimeout 3
Stage 1. Deleting old file from flash memory
->file.remove("main.lua") -> ok
.....................................
->file.close() -> ok
--->>> All down <<<---
```
Connect you terminal program and send command (or you can use -r option, when loading file init.lua)
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

send command (or you can use -d option, when loading file main.lua)
```
dofile("main.lua")
```
waiting some time for get answer from WEB server esp8266.ru

```
> dofile("main.lua")
lua script loaded by luatool 0.4
main.lua ver 1.1
> ip: 	192.168.1.50
send GET to http server...
http server answer:HTTP/1.1 200 OK
Server: nginx
Date: Wed, 26 Nov 2014 22:36:36 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 97597
Connection: keep-alive

```

####Examples:

```
./luatool -p COM4 -f file.lua -t main.lua -b 9600
```
- -p --port - COM1-COM128, default COM3
- -b --baud - baud rate, default 9600
- -f --file from disk file, default name main.lua
- -t --to to flash file, default name main.lua

If use -t option with parameter "init.lua" - autostart init.lua after boot.
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

If you want load and autoexecute file main.lua, command dofile("main.lua"), you can use -d option
```
./luatool -d
```
Typically, place wifi.setmode, wifi.sta.config commands to init.lua file for connecting to you AP with low risk of boot loop, and other code place to main.lua for manually start and debug.
