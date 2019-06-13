# -*- coding: utf-8 -*-

import time
import pandas as pd
import numpy as np

def get_data(slp):

    time.sleep(slp)
    return time.strftime('%S', time.localtime(time.time()))

def creatdata(N):
    now = time.strftime("%H:%M:%S", time.localtime())
    d = pd.date_range(end=now, periods=N, freq='S')
    pydate_array = d.to_pydatetime()
    date_only_array = np.vectorize(lambda s: int(s.strftime('%T').replace(':','')))(pydate_array)
    return date_only_array

if __name__ == '__main__':
    print(creatdata(1200))