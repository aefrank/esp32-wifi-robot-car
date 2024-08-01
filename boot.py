# boot.py -- run on boot-up
import network
import esp
esp.osdebug(None)
import mip

SSID = "UCSD-Conferences"
SSI_PASSWORD = "Conferences2024"

def do_connect():
    # network.WLAN(network.AP_IF).active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print(f"Connecting to WiFi network '{SSID}'... ", end='')
        sta_if.active(True)
        sta_if.connect(SSID, SSI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print("connected!")
    print("IP address:", sta_if.ifconfig()[0])
    
do_connect()
print()
