import os
import numpy as np
import pandas as pd

path = "data2_bin/"  # 原bin文件路径
file = os.listdir(path)  # 读取文件
sampling_rate = 1000  # 采样频率1000hz
channels = 8  # 通道数8
save_path = "data2_csv/"  # 保存路径
os.mkdir(save_path)  # 创建目录
for j in range(len(file)):
    # 依次读取该文件夹中每个bin文件
    file_name = os.listdir(path)[j]
    filename = os.path.splitext(file_name)
    input_name = os.path.join(path, file_name)
    # output_name = os.path.join(input_path,filename[0]) + ".csv"
    ## 读取文件
    data = np.fromfile(input_name, dtype=np.uint8)
    # print(data.shape)#531968
    # reshape
    data.shape = len(data) // 16, 16
    # print('data.shape = ', data.shape)#(33248, 16)
    # mode = 8bit
    out_data = np.zeros((data.shape[0] * 2, channels), dtype='int_')
    # copy and transforme
    out_data = np.copy(data)
    out_data = out_data.flatten()
    out_data = out_data.reshape((data.shape[0] * 2), channels)
    out_csv = pd.DataFrame(out_data)
    # edit colums
    out_csv.columns = ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8']
    # 输出 save，保存为csv格式
    change_name = str(j+1)
    output_name = os.path.join(save_path, change_name) + ".csv"
    out_csv.to_csv(output_name, sep=',', index=0, header=True)  # true指输出第一行索引，如果不需要改为False即可
