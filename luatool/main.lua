print('main.lua ver 1.1')
-- web config
ip="91.201.52.76"
name="esp8266.ru"
port=80
-- web config
function getHTTPreq()
   print('send GET to http server...')
   conn=net.createConnection(net.TCP, false) 
   conn:on("receive", function(conn, payload) print('http server answer:'..payload) end)
   conn:connect(port,ip)
   conn:send("GET / HTTP/1.1\r\nHost: "
   ..name.."\r\nConnection: keep-alive\r\nAccept: */*\r\n\r\n")
end
tmr.alarm(1000, 1, function() 
   if wifi.sta.getip()=="0.0.0.0" then
      print("connecting to AP...") 
   else
      print('ip: ',wifi.sta.getip())
      getHTTPreq()
      tmr.stop()
   end
end)
