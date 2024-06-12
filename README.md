# ESP-01S_Relay
ESP-01S-Relay  Base AP And Wifi
 use xtools.py  [from https://github.com/tony1966/tony1966.github.io/blob/master/test/MicroPython/lib/xtools_orig.py](https://github.com/tony1966/tony1966.github.io/blob/master/test/MicroPython/lib/xtools.py)

 ESP-01S 寫入Micropython 程式 動作步驟
 1.啟動後讀取config.py 連線WIFI。
 2.連線失敗啟動AP，站台IP 192.168.4.1。
 3.連線 192.168.4.1 設定WIFI SSID & PassWord 。
 4.關閉AP 啟動WIFI 連線。

 使用ESP-01s USB轉 ESP8266 WIFI 串口模組 刷入程式，需安裝 CH341SER_LINUX 驅動。 
 https://github.com/juliagoda/CH341SER
 ```
 cd CH341SER_LINUX
 sudo make clean
 sudo make 
 sudo make load 
```
 檢查是否驅動成功
 ```
  ls /dev/ttyUSB*
 ```

 安裝esptool
 ```
 sudo apt update
 sudo apt install python3-pip
 pip3 install esptool
 ```

 檢測ESP-01S 閃存大小
 ```
 esptool.py --port /dev/ttyUSB1 flash_id
 ```
 
 備份bin (我的在ttyUSB0)
 ```
 esptool.py --port /dev/ttyUSB0 read_flash 0 0x100000 backup.bin
 ```

 還原
 ```
 esptool.py --port /dev/ttyUSB0 write_flash --flash_size=detect 0 backup.bin
 ```
 或
 ```
 esptool.py --port /dev/ttyUSB0 write_flash --flash_size 1MB 0 backup.bin
 ```
 刷bin ESP8266_GENERIC-20220618-v1.19.1.bin
 ```
 esptool.py --port /dev/ttyUSB1 --baud 115200 write_flash --flash_size=detect 0 ESP8266_GENERIC-FLASH_1M-20240222-v1.22.2.bin
 ```

 上傳檔案至ESP-01S 使用ampy 先安裝 pip install ampy  or pip3 install ampy
 ```
 ampy --port /dev/ttyUSB0 put app.py app.py
 ampy --port /dev/ttyUSB0 put config.py config.py
 ampy --port /dev/ttyUSB0 put main.py main.py
 ampy --port /dev/ttyUSB0 put mydecode.py mydecode.py
 ampy --port /dev/ttyUSB0 put simple.py simple.py
 ampy --port /dev/ttyUSB0 put xtools.py xtools.py
 ```

 即可使用Thonny idea 開發
 

 
