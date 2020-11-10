import numpy as np
from datetime import datetime,timedelta
def get_nearest_time(_ttime,_ftimes):
    ttime=datetime.strptime(_ttime,'%Y-%m-%d-%H-%M-%S-%f')
    tzero=timedelta()
    tdelta1=timedelta(days=1)
    tdelta1_index=0
    tdelta2=timedelta(days=1)
    tdelta2_index=0
    for index,_ftime in enumerate(_ftimes):
        ftime=datetime.strptime(_ftime,'%Y-%m-%d-%H-%M-%S-%f')
        tdelta=ftime-ttime
        if(tdelta==tzero):
            tdelta1=tdelta
            tdelta1_index=index
            break
        elif(tdelta<tzero and ((abs(tdelta)<abs(tdelta1)))):
            tdelta1=tdelta
            tdelta1_index=index
        elif(tdelta>tzero):
            tdelta2=tdelta
            tdelta2_index=index
            break
    if (index==(_ftimes.shape[0]-1)):
        raise Exception("Out of bound")
    if (abs(tdelta1)<abs(tdelta2)):
        return tdelta1_index
    return tdelta2_index

def split_data(vtimes:np.array,atimes:np.array,startpoints:list,period:timedelta,delta:timedelta):
    ret=list()
    try:
        for spoint,nums in startpoints:
            _vstart_point_time = vtimes[spoint]
            vstart_point_time = datetime.strptime(_vstart_point_time, '%Y-%m-%d-%H-%M-%S-%f')
            for i in range(nums):
                if (i==0):
                    vstime_index=spoint
                    _vstime=_vstart_point_time
                else:
                    vstime_index = get_nearest_time((vstart_point_time+delta*i).strftime('%Y-%m-%d-%H-%M-%S-%f'),vtimes)
                    _vstime=vtimes[vstime_index]
                vstime = datetime.strptime(_vstime, '%Y-%m-%d-%H-%M-%S-%f')
                desired_vendtime=vstime+period
                _desired_vendtime=desired_vendtime.strftime('%Y-%m-%d-%H-%M-%S-%f')
                vendtime_index=get_nearest_time(_desired_vendtime,vtimes)
                _vetime=vtimes[vendtime_index]
                astime_index=get_nearest_time(_vstime,atimes)
                aetime_index=get_nearest_time(_vetime,atimes)
                ret.append([(vstime_index,vendtime_index),(astime_index,aetime_index)])
    finally:
        return ret
def normalize(data:np.array):
    return (data-np.mean(data))/np.std(data)
if __name__=='__main__':
    ttimes=np.loadtxt('/root/workspace/LLAP-Aux/Documents/11-06-19-56-47-vlog-time.txt',dtype=str)
    ftimes=np.loadtxt('/root/workspace/LLAP-Aux/Documents/11-06-19-56-47-alog-time.txt',dtype=str)
    data_point=split_data(vtimes=ttimes,atimes=ftimes,startpoints=[(60,1),[600,2]],period=timedelta(seconds=5),delta=timedelta(seconds=2))
    print(data_point)
    for camera,arduino in data_point:
        print(camera[1]-camera[0])
    for camera,arduino in data_point:
        print(arduino[1]-arduino[0])
    print('End')