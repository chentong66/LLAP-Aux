import numpy as np
from matplotlib import pyplot as plt
def subplot(datas:list):
    num=len(datas)
    for i in range(0,num):
        plt.subplot(num,1,i+1)
        x=range(0,datas[i].shape[0])
        plt.plot(x,datas[i])
    plt.show()
def data_transform(data:np.array,desired_num:int):
    num=data.shape[0]
    if (num==desired_num):
        return data
    elif (num>desired_num):
        half=(num-desired_num)//2
        padding=(num-desired_num)%2
        return data[0+half+padding:num-half]
    else:
        ndata=np.zeros(desired_num)
        half=(desired_num-num)//2
        padding=(desired_num-num)%2
        ndata[half+padding:desired_num-half]=data
        ndata[0:half+padding]=data[0]
        ndata[desired_num-half:desired_num]=data[-1]
        return ndata

def normalize(data: np.array):
    return (data - np.mean(data)) / np.std(data)

def construct_data(cppg:np.array,cdesired_num:int,cmax_difference:int,appg:np.array,adesired_num:int,amax_difference:int,data_points:list):
    cppg_ret=list()
    appg_ret=list()
    for dpoint in data_points:
        if (abs(dpoint[0][1]-dpoint[0][0]-cdesired_num)>cmax_difference) or (abs(dpoint[1][1]-dpoint[1][0]-adesired_num)>amax_difference):
            continue
        cppg_ret.append(normalize(data_transform(cppg[dpoint[0][0]:dpoint[0][1]],cdesired_num)))
        appg_ret.append(normalize(data_transform(appg[dpoint[1][0]:dpoint[1][1]],adesired_num)))
    return np.array(cppg_ret),np.array(appg_ret)

def assemble_data(dir:str,files:list):
    gdata=[]
    ddata=[]
    for file in files:
        gdata.append(np.loadtxt(dir+file+'camera.np'))
        ddata.append(np.loadtxt(dir+file+'arduino.np'))
    x=range(1,len(files))
    gnp=gdata[0]
    dnp=ddata[0]
    print(gnp.shape)
    for i in x:
        print(gdata[i].shape)
        gnp=np.vstack([gnp,gdata[i]])
        dnp=np.vstack([dnp,ddata[i]])
    return [gnp,dnp]
if __name__=='__main__':
    dir='/tmp/orig_data/'
    files=[
        '11-11-20-05-31-',
        '11-11-20-07-08-',
        '11-11-20-08-43-',
        '11-11-20-10-22-'
    ]
    data=assemble_data(dir,files)
    for i in range(0,3):
        data[0]=np.vstack([data[0],data[0]])
        data[1]=np.vstack([data[1],data[1]])
    np.savetxt('/tmp/n1.txt',data[0])
    np.savetxt('/tmp/n2.txt',data[1])

    print('End')