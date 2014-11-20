print('esp config from init.lua script ver 1.0')
wifi.setmode(wifi.STATION)
print('set mode=STATION (',wifi.getmode(),')')
print('MAC=',wifi.sta.getmac())
print('set wifi')
-- wifi config
wifi.sta.config("BRUC2","MasterPasswordVictorEvaVarvara")
-- wifi config
print('get ip ',wifi.sta.getip())
print('start TCP client...')
conn=net.createConnection(net.TCP, false) 
conn:on("receive", function(conn, payload) print("data ",payload) end )
-- web config
conn:connect(80,"70.38.12.79")
conn:send("GET / HTTP/1.1\r\nHost: esp8266.com\r\n")
-- web config
