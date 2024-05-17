import os
import numpy as np
import pandas as pd

path = "data2_csv/"  # 原csv文件路径
file = os.listdir(path)  # 读取文件

for j in range(len(file)):
    # 依次读取该文件夹中每个bin文件
    file_single = os.listdir(path)[j]
    data = np.array(pd.read_csv(path+file_single))
    data = data[:1200, :4]
    out_data = np.copy(data)
    out_csv = pd.DataFrame(out_data)
    out_csv.columns = ['ch1', 'ch2', 'ch3', 'ch4']
    out_csv.to_csv(path+os.listdir(path)[j], index=False,header=True)
