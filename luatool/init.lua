print('init.lua ver 1.1')
wifi.setmode(wifi.STATION)
print('set mode=STATION (mode=',wifi.getmode(),')')
print('MAC=',wifi.sta.getmac())
print('set wifi')
-- wifi config start
wifi.sta.config("BRUC2","MasterPasswordVictorEvaVarvara")
-- wifi config end
