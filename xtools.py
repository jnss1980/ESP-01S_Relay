# xtools.py
from machine import Pin
import urandom, math
import time, network, urequests
import ubinascii
import machine
import config
import ntptime
from mydecode import mydecode
   
def connect_wifi_led(ssid=config.SSID, passwd=config.PASSWORD, timeout=15):
    wifi_led=Pin(2, Pin.OUT, value=1)
    sta=network.WLAN(network.STA_IF)
    sta.active(True)
    start_time=time.time() # 記錄時間判斷是否超時
    if not sta.isconnected():
        print("Connecting to network...")
        sta.connect(ssid, passwd)
        while not sta.isconnected():
            wifi_led.value(0)
            time.sleep_ms(150)
            wifi_led.value(1)
            time.sleep_ms(150)
            # 判斷是否超過timeout秒數
            if time.time()-start_time > timeout:
                print("Wifi connecting timeout!")
                break
    if sta.isconnected():
        for i in range(25):   # 連線成功 : 快閃 5 秒
            wifi_led.value(0)
            time.sleep_ms(100)
            wifi_led.value(1)
            time.sleep_ms(100)
        print("network config:", sta.ifconfig())
        return sta.ifconfig()[0] 

def set_ap(led=2):
    html='''
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
      </head>
      <body>
        %s
      </body>
    </html>
    '''
    form='''
        <form method='get' action='/update_ap' 
        style='width: max-content; margin: 10px auto'>
          <h2 style='text-align: center; font-size: 20px'>設定 WiFi 基地台</h2>
          SSID:<input type='text' name='ssid' style='width: 100%; font-size: 16px'><br/>
          PWD:<input type='text' name='pwd' style='width: 100%; font-size: 16px'><br/>          
          HomeAssIP:<input type='text' name='homeassip' style='width: 100%; font-size: 16px'><br/>
          HomeAssID:<input type='text' name='homeassid' style='width: 100%; font-size: 16px'><br/>
          HomeAssPWD:<input type='text' name='homeasspwd' style='width: 100%; font-size: 16px'><br/>          
          <button type="submit" style='width:100%;font-size: 16px'>連線</button>
        </form>
        <hr/>
        設備:<a href='/relay_ap?acc=on'>啟動</a> _ <a href='/relay_ap?acc=off'>停止</a><br/>        
    '''
    ok='''
       <h2>WiFi 連線成功<br>IP : <a href={0}>{0}</a></h2>
       <a href=192.168.4.1>
         <button style="width:100%;font-size: 16px">重新設定</button>
       </a>              
    '''
    ng='''
       <h2 style="text-align: center;">WiFi 基地台連線失敗<br> 
       按 Reset 鈕後重新設定</h2>
       <a href="192.168.4.1">
         <button style="width:100%;font-size: 16px">重新設定</button>
       </a>   
    '''
    wifi_led=Pin(led, Pin.OUT, value=1)  # 預設熄滅板上 LED
    ap=network.WLAN(network.AP_IF)       # 開啟 AP 模式
    ap.active(True)
    sta=network.WLAN(network.STA_IF)     # 開啟 STA 模式
    sta.active(True)
    import socket
    addr=socket.getaddrinfo('192.168.4.1', 80)[0][-1] # 傳回 (ip, port)
    s=socket.socket()  # 建立伺服端 TCP socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 網址可重複請求
    s.bind(addr)  # 綁定 192.168.4.1 的 80 埠
    s.listen(3)   # 最多同時 5 個連線
    print('網頁伺服器正在監聽 : ', addr)
    while True:   # 監聽 192.168.4.1 的 80 埠
        cs, addr=s.accept()  
        print('發現來自客戶端的連線 : ', addr)
        data=cs.recv(1024)      
        request=str(data, 'utf8')   
        print(request, end='\n')
        if request.find('update_ap?') == 5:  # 檢查是否為更新之 URL 
            # 擷取請求參數中的 SSID 與密碼
            para=request[request.find('ssid='):request.find(' HTTP/')]
            ssid=para.split('&')[0].split('=')[1]
            pwd=para.split('&')[1].split('=')[1]
            homeassip=""
            homeassid=""
            homeasspwd=""
            try:
                homeassip=para.split('&')[2].split('=')[1]
            except:
                homeassip=""
            try:
                homeassid=para.split('&')[3].split('=')[1]
            except:
                homeassid=""
            try:
                homeasspwd=para.split('&')[4].split('=')[1]
            except:
                homeasspwd=""
            print('ssid:'+ssid+'\n')
            print('pwd:'+pwd+'\n')
            print('homeassip:'+homeassip+'\n')
            print('homeassid:'+homeassid+'\n')
            print('homeasspwd:'+homeasspwd+'\n')           
            
            sta.connect(mydecode(ssid), mydecode(pwd))       # 連線 WiFi 基地台
            start_time=time.time()       # 紀錄起始時間  
            while not sta.isconnected(): # 連線 WiFi (15 秒)
                wifi_led.value(0)  # 讓板載 LED 閃爍
                time.sleep_ms(300)
                wifi_led.value(1)
                time.sleep_ms(300)                
                if time.time()-start_time > 15: # 是否超過連線秒數
                    print('WiFi 連線逾時!')
                    break  # 逾時跳出無限迴圈
            # 確認是否連線成功
            if sta.isconnected():     # WiFi 連線成功
                print('WiFi 連線成功 : ', sta.ifconfig())
                ip=sta.ifconfig()[0]  # 取得 ip
                print('取得 IP : ' + ip)
               
                with open('config.py', 'w', encoding='utf-8') as f:
                    val='SSID="'+mydecode(ssid)+'"\n'
                    val+='PASSWORD="'+mydecode(pwd)+'"\n'
                    val+='homeassip="'+mydecode(homeassip)+'"\n'
                    val+='homeassid="'+mydecode(homeassid)+'"\n'
                    val+='homeasspwd="'+mydecode(homeasspwd)+'"\n'
                    f.write(val) # 更新設定檔
                cs.send(html % ok.format(ip))  # 回應連線成功頁面
                for i in range(25):   # 連線成功 : 快閃 5 秒
                    wifi_led.value(0)
                    time.sleep_ms(100)
                    wifi_led.value(1)
                    time.sleep_ms(100)
                cs.close()
                s.close()
                return ip
            else:
                print('WiFi 連線失敗 : 請按 Reset 鈕後重設.')
                wifi_led.value(1)     # 連線失敗 : 熄滅 LED
                cs.send(html % ng)    # 回應連線失敗頁面
                cs.close()
                s.close()
                return None
        elif request.find('relay_ap?') == 5:
            RELAY_PIN = Pin(0,Pin.OUT)
            acc=request[request.find('acc='):request.find(' HTTP/')]
            if acc.split('=')[1] == 'on':
                RELAY_PIN.value(0)
            else:
                RELAY_PIN.value(1)
            cs.send(html % form)            
        else:  # 顯示設定 WiFi 頁面
            cs.send(html % form)  # 回應設定 WiFi 頁面
        cs.close()
        del cs, addr, data, request

