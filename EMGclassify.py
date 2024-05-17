import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from scipy import signal
from scipy.signal import butter, filtfilt
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
X_train = []
y_train = []
X_test = []
y_test = []

# 设置滤波器参数
sampling_frequency = 1000.0  # 采样频率
filter_order = 4  # 滤波器阶数
low_cutoff = 10  # 低截止频率（单位：Hz）
high_cutoff = 300  # 高截止频率（单位：Hz）

path1 = "data1_csv/"  # 原csv文件路径
path2 = 'data2_csv/'
file1 = os.listdir(path1)  # 读取文件
file2 = os.listdir(path2)
file1_n = []
file2_n = []

for j in range(len(file1)):
    file1_single = file1[j]
    filename, _ = os.path.splitext(file1_single)
    file1_n.append(int(filename))

for j in range(len(file2)):
    file2_single = file2[j]
    filename, _ = os.path.splitext(file2_single)
    file2_n.append(int(filename))
file1_n.sort()
file2_n.sort()


# 低通滤波器
def low_pass_filter(data, cutoff_freq, sampling_freq, order=5):
    # 计算归一化的截止频率
    normalized_cutoff_freq = cutoff_freq / (0.5 * sampling_freq)
    # 使用巴特沃斯滤波器设计滤波器系数
    b, a = butter(order, normalized_cutoff_freq, btype='low', analog=False)
    # 应用滤波器
    filtered_data = filtfilt(b, a, data, axis=1)
    return filtered_data


# 带通滤波器
def bandpass_filter(data, low_cutoff, high_cutoff, sampling_freq, order=5):
    # 计算归一化的截止频率
    normalized_low = low_cutoff / (0.5 * sampling_frequency)
    normalized_high = high_cutoff / (0.5 * sampling_frequency)
    b, a = signal.butter(order, [normalized_low, normalized_high], btype='bandpass')
    # 应用滤波器
    filtered_data = filtfilt(b, a, data, axis=1)
    return filtered_data


# 转为psd
def transform_psd(data):
    _, psd = signal.welch(data)
    return psd


# 训练集和测试集
def X_train_test(X_train, X_test, file1, file2, path1, path2, file1_n, file2_n):
    for j in range(len(file1)):
        # 依次读取该文件夹中每个csv文件
        data1 = np.array(pd.read_csv(path1 + str(file1_n[j]) + '.csv'))
        if j < 25:
            X_train.append(data1)
        else:
            X_test.append(data1)
    for j in range(len(file2)):
        # 依次读取该文件夹中每个csv文件
        data2 = np.array(pd.read_csv(path2 + str(file2_n[j]) + '.csv'))
        if j < 25:
            X_train.append(data2)
        else:
            X_test.append(data2)
    return X_train, X_test


X_train, X_test = X_train_test(X_train, X_test, file1, file2, path1, path2, file1_n, file2_n)
X_train = np.array(X_train).reshape(50, -1)
X_test = np.array(X_test).reshape(50, -1)

# 标准化
scaler = StandardScaler()  # 创建一个StandardScaler对象用于数据标准化
X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)

# 转为psd
X_train = transform_psd(X_train)
X_test = transform_psd(X_test)

# 滤波
X_train = bandpass_filter(X_train, low_cutoff, high_cutoff, sampling_frequency, filter_order)
X_test = bandpass_filter(X_test, low_cutoff, high_cutoff, sampling_frequency, filter_order)

# 标签
y_train = np.zeros((50, 2))
y_train[:25, 0] = 1
y_train[25:, 1] = 1

y_test = np.zeros((50, 2))
y_test[:25, 0] = 1
y_test[25:, 1] = 1

# 决策树模型训练和预测
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 评估模型性能
accuracy = accuracy_score(y_test, y_pred)
print("Test Accuracy: {}".format(accuracy))
