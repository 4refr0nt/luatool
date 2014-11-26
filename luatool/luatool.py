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

version="0.3"

def writer(data):
    time.sleep(0.1)
    data = data.split("--")
    if len( data[0] ) > 0:
        s.write("file.writeline([[" + data[0] + "]])\r")
        sys.stdout.write(data[0])
        sys.stdout.write("\r\n")

def usage():
    sys.stderr.write("""USAGE: %s [options]
    ESP8266 lua script downloader.
 
    options:
    -p, --port=PORT: port, a number, default = 0 or a device name
    -b, --baud=BAUD: baudrate, default 9600
    -f, --file=FROM DISK FILE: lua script file, default main.lua
    -t, --to=TO FLASH FILE: lua script file in flash, default main.lua
 
 """ % sys.argv[0])
 
if __name__ == '__main__':
    #initialize with defaults
    port  = "COM3"
    baudrate = 9600
    fn = "main.lua"
    ft = "main.lua"

    #parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],
            "hp:b:f:t:",
            ["help", "port=", "baud=", "file=", "to="]
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
        elif o in ("-t", "--fo"):     #specified file to
            ft = a
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
    sys.stderr.write("start writing...\r\n")
    s.write("file.open(\""+ft+"\", \"w\")\r")    # if file not found, we create
    s.write("file.writeline([[print(1)]])\r")    # not empty file
    s.write("file.close()\r")
    s.write("file.open(\""+ft+"\", \"w+\")\r")   # write from begin of file
    s.write("file.writeline([[print(\"lua script loaded by luatool " + version + "\")]])\r")
    line = f.readline()
    while line != '':
        writer(line.strip())
        line = f.readline()
    time.sleep(0.1)
    s.write("file.close()\r")
    s.close()
    f.close()
    sys.stderr.write("All down.\r\n")
