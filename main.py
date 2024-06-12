import xtools    
import config
import gc
import app

def gcfree():
    free_memory = gc.mem_free()
    allocated_memory = gc.mem_alloc()
    print("可用記憶體:", free_memory)
    print("已分配記憶體:", allocated_memory)
   
def onStartApp():
    gcfree()    
    ip=xtools.connect_wifi_led(config.SSID, config.PASSWORD)
    if not ip:
        gcfree()    
        ip=xtools.set_ap()   # 這是我增添到 xtools 的自訂函式
        if not ip:  
            print('無法連線 WiFi 基地台')
        else:
            print("WiFi 連線成功! IP : ", ip)
            print('啟動AP Relay')
            gcfree()    
            app.runApp()
            
    else:
        print("WiFi 連線成功! IP : ", ip)
        print('啟動AP Relay')
        gcfree()    
        app.runApp()
    
onStartApp()
    
