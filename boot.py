# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

def connectAp(ssid,pwd):
    import network
    sta = network.WLAN(network.STA_IF)
    if not sta.isconnected():
        sta.active(True)
        sta.connect(ssid,pwd)
        while not sta.inconnected():
            pass
    print("network config:",sta.ifconfig())
connectAp("cxy","111222333")