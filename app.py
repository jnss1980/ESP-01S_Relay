from machine import Pin,Timer
from simple import MQTTClient
import time
import config
def MQTT_callback(topic, msg):    
    print('topic: {}'.format(topic))
    print('msg: {}'.format(msg))
    RELAY_PIN = Pin(0,Pin.OUT)
    if msg == b'ON' :        
        RELAY_PIN.value(0)
        print('ON')
    
    if msg == b'OFF' :        
        RELAY_PIN.value(1)
        print('OFF')
#接收数据任务·
def MQTT_Rev(tim):
    client.check_msg()
def connect_and_subscribe():
    global client
    CLIENT_ID = 'WalnutPi-LED'
    SERVER=config.homeassip
    PORT=1883
    USER=config.homeassid
    PASSWORD=config.homeasspwd
    client = MQTTClient(CLIENT_ID, SERVER, PORT, USER, PASSWORD)
    client.set_callback(MQTT_callback)  #配置回调函数
    client.connect()
    TOPIC = "homeassistant/light/picow1_led/config"
    mssage = """{
                  "name": "led",
                  "device_class": "LIGHT",
                  "command_topic": "picow1_led/light/state",
                  "unique_id": "picow1_led",
                  
                  "device": {
                            "identifiers": "picow_1",
                            "name": "picow1"
                            }
                }"""
    client.publish(TOPIC, mssage)
    #订阅主题 
    TOPIC = 'picow1_led/light/state' # TOPIC名称
    client.subscribe(TOPIC) #订阅主题
def reconnect():
    print('Attempting to reconnect...')
    time.sleep(5)
    try:
        connect_and_subscribe()
    except OSError as e:
        print('Failed to reconnect: %s' % str(e))
def runApp():
    try:
        connect_and_subscribe()
    except OSError as e:
        print('Failed to connect: %s' % str(e))
        reconnect()

    tim = Timer(0)
    # 初始化定時器：周期為 20000 ms (20 秒)，模式為週期性，並設置回調函數
    tim.init(period=20000, mode=Timer.PERIODIC, callback=MQTT_Rev)
    # 主循環
    while True:
        try:
            client.check_msg()  # 持續檢查消息
        except OSError as e:
            print('Failed to check messages in main loop: %s' % str(e))
            reconnect()
        time.sleep(1)
