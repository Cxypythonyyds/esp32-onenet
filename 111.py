from umqtt.simple import MQTTClient
from machine import Pin,Timer
import dht

import machine
from time import sleep
import utime
import utime
try:
  import usocket as socket
except:
  import socket
import network
import esp
esp.osdebug(None)

import gc


d = dht.DHT11(Pin(4))
temp = 0
hum = 80
led = Pin(26,Pin.OUT)
led_state = 0

url = "https://api.heclouds.com/devices/738116528/datapoints"



#服务器配置信息
SERVER = "183.230.40.39"
PORT = 6002
USER = "592902"
CLIENT_ID = "1069265516"
PASSWORD = "zxc"
topic_dp = b"$dp"

def sub_cb(topic,msg):
    print(topic,msg)
    if msg == b"on":
        led.value(1)
        led_state = 1
    elif msg == b"off":
        led.value(0)
        led_state = 0
    message = '{"led_state":%d}'%(led_state)
    message = pack_msg(message)
    c.publish(topic_dp,message)

c = MQTTClient(CLIENT_ID,SERVER,PORT,USER,PASSWORD)
c.set_callback(sub_cb)
c.connect()

def pack_msg(message):#将消息封装为ONENET要求的格式
    msglen=len(message)
    tmp=[0,0,0]
    tmp[0]='\x03'
    tmp[1]=msglen>>8
    tmp[2]=msglen&0XFF
    message="%c%c%c%s"%(tmp[0],tmp[1],tmp[2],message)            
    return message

def update(t=None):
     global temp,hum
     try:
         d.measure()
         temp = d.temperature()
         hum = d.humidity()
         message = '{"temp":%d,"humid":%d}'%(temp,hum)
         message = pack_msg(message)
         c.publish(topic_dp,message)
     except Exception as e:
         print(e)
     
    
tm = Timer(0)
tm.init(period=5000,mode=Timer.PERIODIC,callback=update)

    
    
makerobo_DO        = 27     # 传感器数字IO口
led_onboard = machine.Pin(16,machine.Pin.OUT)
buzzer = machine.Pin(25,machine.Pin.OUT)
buzzer.value(1)
# 设置风扇管脚PIN
Makerobo_MotorPin1   =  machine.Pin(32,machine.Pin.OUT)
#上床下床自动亮灯
Pin2 = machine.Pin(2,machine.Pin.OUT)  
makerobo_pirPin = 33    # PIR人体热释电管脚PIN
pir = Pin(makerobo_pirPin, Pin.IN) # 将makerobo_pirPin设置为输入

# 初始化工作
def makerobo_setup():
    global DO
    DO = Pin(makerobo_DO,Pin.IN) # 设置火焰传感器数字IO口为输入模式

# 打印信息，打印出火焰传感器的状态值
def makerobo_Print(x):
    if x == 1:      # 安全
        print ('')
        print ('   *******************')
        print ('   *  Makerobo Safe~ *')
        print ('   *******************')
        print ('')
        led_onboard.value(0)
        buzzer.value(1)
        utime.sleep_ms(5000)
        Makerobo_MotorPin1.value(0)
    if x == 0:     # 有火焰
        print ('')
        print ('   ******************')
        print ('   * Makerobo Fire! *')
        print ('   ******************')
        print ('')
        led_onboard.value(1)
        buzzer.value(0)
        Makerobo_MotorPin1.value(1)
        
        
# 循环函数
def makerobo_loop():
    makerobo_status = 1      # 状态值
    
    # 无限循环
    while True:
        c.check_msg()
        # 读取传感器数字IO口
        makerobo_tmp = DO.value()
        if makerobo_tmp != makerobo_status:     # 判断状态发生改变
            makerobo_Print(makerobo_tmp)        # 打印出火焰传感器的提示信息
            makerobo_status = makerobo_tmp               # 当前状态值作为下次状态值进行比较，避免重复打印

        sleep(0.2)                         # 延时200ms
        pir_val = pir.value()
        if pir_val==1:
            
            Pin2.value(1)
            utime.sleep_ms(5000)
        else :
            Pin2.value(0)

            
        

# 程序入口
if __name__ == '__main__':
    makerobo_setup() # 初始化
    makerobo_loop()  # 循环函数    