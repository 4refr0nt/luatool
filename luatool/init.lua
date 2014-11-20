print('esp config from init.lua script ver 1.0')
wifi.setmode(wifi.STATION)
print('set mode=STATION (mode=',wifi.getmode(),')')
print('MAC=',wifi.sta.getmac())
print('set wifi')
-- wifi config
wifi.sta.config("ssid","MasterPassword")
-- wifi config
print('waiting for WiFi connection...')
i=0
j=0
success = 1
timer0 = tmr.now()
while string.find(wifi.sta.getip(),"0.0.0") > 0 do
      i = i + 1                           -- do nothing, connection waiting
      if i > 1000 then                    -- number overflow disabled
         i = 0
      end
      if tmr.now() - timer0 > 10000 then -- timer overflow disabled
         j = j + 1       -- 0.01 sec
         timer0 = tmr.now()
      end
      if j > 500 then -- 5sec
         print('timeout')
         success = 0
         break
      end
end
if success > 0 then
   print('get ip ',wifi.sta.getip())
   print('start TCP client...')
   conn=net.createConnection(net.TCP, false) 
   conn:on("receive", function(conn, payload) print("data ",payload) end )
   -- web config
   conn:connect(80,"70.38.12.79")
   conn:send("GET / HTTP/1.1\r\nHost: esp8266.com\r\n")
   -- web config
else
   print('no WiFi connection - done.')
end
