# -*- coding: utf-8 -*-
import binascii
import serial
import time



# if __name__ == '__main__':
def get_serialData(comNum,bot):
    ser = serial.Serial(comNum,bot)
    strInput = "01 04 00 00 00 08 F1 CC"
    try:  # 如果输入不是十六进制数据--
        n = ser.write(bytes.fromhex(strInput))
    except:  # --则将其作为字符串输出
        n = ser.write(bytes(strInput, encoding='utf-8'))

    time.sleep(0.1)  # sleep() 与 inWaiting() 最好配对使用
    num = ser.inWaiting()
    # print("num:", num)

    if num:
        try:  # 如果读取的不是十六进制数据--
            data = str(binascii.b2a_hex(ser.read(num)))[2:-1]  # 十六进制显示方法2
            # print("data:",int(data[6:10],16))
            result = int(data[6:10],16)
            # return  int(data[6:10],16)
        except:  # --则将其作为字符串读取
            data = ser.read(num)
            # print("str:",int(data[6:10],16))
            result = int(data[6:10], 16)
            # return int(data[6:10], 16)

    serial.Serial.close(ser)
    # result0 = (result*(10-0.45)/4095)*697837.0616+628.9686
    return result

if __name__ == '__main__':
    while True:
        time.sleep(1)
        # get_serialData()
        print(get_serialData('com3',9600))