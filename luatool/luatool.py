#!/usr/bin/env python
#
# ESP8266 luatool
# Author e-mail: 4ref0nt@gmail.com
# Site: http://esp8266.ru
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys
import serial
import getopt
import time

version="0.5"

def writeln(data, check = 1):
    if s.inWaiting() > 0:
       s.flushInput()
    if len( data ) > 0:
        sys.stdout.write("\r\n->")
        sys.stdout.write(data.split("\r")[0])
    s.write(data)
    time.sleep(0.3)
    if check > 0 :
       line = ''
       char = ''
       while char != chr(62) : # '>'
           char = s.read(1)
           if char == '' :
               raise Exception('No proper answer from LuaMCU')
           if char == chr(13) or char == chr(10) :
              if line != '':
                 if line+'\r' == data :
                    sys.stdout.write(" -> ok")
                 else :
                    if line[:4] == "lua:" :
                       sys.stdout.write("\r\n\r\nLUA ERROR: %s" % line)
                       raise Exception('ERROR from LUA interpreter\r\n\r\n')
                    else :
                       data = data.split("\r")[0]
                       sys.stdout.write("\r\n\r\nERROR")
                       sys.stdout.write("\r\n send string    : '%s'" % data)
                       sys.stdout.write("\r\n expected echo  : '%s'" % data)
                       sys.stdout.write("\r\n but got answer : '%s'" % line)
                       sys.stdout.write("\r\n\r\n")
                       raise Exception('Error sending data to LuaMCU\r\n\r\n')
                 line = ''
           else :
              line += char
    else: 
       sys.stdout.write(" -> send without check")
def writer(data):
    writeln("file.writeline([[" + data + "]])\r")

def usage():
    sys.stderr.write("""USAGE: %s [options]
    ESP8266 lua script downloader.
 
    options:
    -p, --port=PORT: port, a number, default = 0 or a device name
    -b, --baud=BAUD: baudrate, default 9600
    -f, --file=FROM DISK FILE: lua script file, default main.lua
    -t, --to=TO FLASH FILE: lua script file in flash, default main.lua
    -r  --restart - auto restart module, execute node.restart() after file load 
    -d  --dofile  - auto run, execute dofile('file') after file load 
 
 """ % sys.argv[0])
 
if __name__ == '__main__':
    #initialize with defaults
    port  = "COM3"
    baudrate = 9600
    fn = "main.lua"
    ft = "main.lua"
    autorun = 0
    autorestart = 0

    #parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],
            "hp:b:f:t:rd",
            ["help", "port=", "baud=", "file=", "to=", "restart"]
        )
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    
    for o, a in opts:
        if o in ("-h", "--help"):       #help text
            usage()
            sys.exit()
        elif o in ("-p", "--port"):     #specified port
            try:
                port = int(a)
            except ValueError:
                port = a
        elif o in ("-b", "--baud"):     #specified baudrate
            try:
                baudrate = int(a)
            except ValueError:
                raise ValueError, "Baudrate must be a integer number, not %r" % a
        elif o in ("-f", "--file"):     #specified file from
            fn = a
        elif o in ("-t", "--fo"):       #specified file to
            ft = a
        if o in ("-r", "--restart"):    # autorestart
            autorestart = 1
        if o in ("-d", "--dofile"):     # autorun
            autorun = 1
    #open file
    try:
        f = open(fn,"rt")
    except:
        sys.stderr.write("Could not open input file \"%s\"\n" % fn)
        sys.exit(1)
    #open the port
    try:
        s = serial.Serial(port, baudrate)
    except:
        sys.stderr.write("Could not open port %s\n" % (port))
        sys.exit(1)
    sys.stderr.write("Downloader start\r\n")

#    try:
#        lf = open(sys.argv[0].split(".")[0]+".log","w")
#    except:
#         log = 0

    s.timeout = 3
    sys.stderr.write("Set timeout %s\r\n" % s.timeout)
    s.interCharTimeout = 3
    sys.stderr.write("Set interCharTimeout %s\r\n" % s.interCharTimeout)
    sys.stderr.write("Stage 1. Deleting old file from flash memory")
    writeln("file.open(\""+ft+"\", \"w\")\r")
    writeln("file.close()\r")
    writeln("file.remove(\""+ft+"\")\r")
    sys.stderr.write("\r\nStage 2. Creating file in flash memory and write first line")
    writeln("file.open(\""+ft+"\", \"w+\")\r")
    line = f.readline()
    sys.stderr.write("\r\nStage 3. Start writing data to flash memory...")
    while line != '':
        writer(line.strip())
        line = f.readline()
    f.close()
    sys.stderr.write("\r\nStage 4. Flush data and closing file")
    writeln("file.flush()\r")
    writeln("file.close()\r")
    if autorestart > 0 :
       writeln("node.restart()\r")
    if autorun > 0 : # never exec if autorestart=1
       writeln("dofile(\""+ft+"\")\r",0)
    s.close()
    sys.stderr.write("\r\n--->>> All down <<<---\r\n")
