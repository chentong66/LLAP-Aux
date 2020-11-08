import serial
import sys
import os
import datetime
if __name__=='__main__':
    if len(sys.argv)<2:
        print('Usage:python3 *.py file_to_save')
        quit()
    fall=open(sys.argv[1],'w')
    fppg=open(sys.argv[1]+'_ppg','w')
    ftime=open(sys.argv[1]+'_time','w')
    ser=serial.Serial('/dev/ttyUSB0',baudrate=115200)
    while True:
        try:
            line=str(ser.readline().strip(),'utf-8')
        except:
            continue
        time=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        ppg=line.split(',')[1]
        fall.writelines(line+','+time+'\n')
        fppg.writelines(ppg+'\n')
        ftime.writelines(time+'\n')
        print(line)
    fall.close()
    fppg.close()
    ftime.close()
