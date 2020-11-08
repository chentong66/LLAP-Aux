import pyqtgraph as pg
import numpy as np
import array
import serial
import sys
import datetime
if len(sys.argv)<2:
    print('Usage python3 *.py file_to_save')
    quit()
app = pg.mkQApp()#建立app
win = pg.GraphicsWindow()#建立窗口
win.setWindowTitle('PPG-serial')
win.resize(800, 500)#小窗口大小

data = array.array('f') #可动态改变数组的大小,double型数组
historyLength = 2000#横坐标长度
p = win.addPlot()#把图p加入到窗口中
p.showGrid(x=True, y=True)#把X和Y的表格打开
p.setRange(xRange=[0,historyLength], yRange=[-100, 1000], padding=0)
p.setLabel(axis='left', text='y / V')#靠左
p.setLabel(axis='bottom', text='x / point')
p.setTitle('y = sin(x)')#表格的名字
curve = p.plot()#绘制一个图形
ser=serial.Serial('/dev/ttyUSB0',baudrate=115200)
fall=open(sys.argv[1],'w')
fppg=open(sys.argv[1]+'_ppg','w')
ftime=open(sys.argv[1]+'_time','w')
def plotData():
    line=str(ser.readline().strip(),'utf-8')
    ppg=float(line.split(',')[2])
    time=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    fall.writelines(line+','+time+'\n')
    fppg.writelines(str(ppg)+'\n')
    ftime.writelines(time+'\n')
    print(line+','+time)
    if len(data)<historyLength:
        data.append(ppg)
    else:
        data[:-1] = data[1:]#前移
        data[-1] = ppg
    curve.setData(data)
timer = pg.QtCore.QTimer()
timer.timeout.connect(plotData)#定时调用plotData函数
timer.start(2)#多少ms调用一次
app.exec_()
fall.close()
fppg.close()
ftime.close()
