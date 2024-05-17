import numpy as np
import tkinter as tk
import cv2
from tkinter import font as tkfont
from PIL import ImageTk, Image

path = 'C:\\Users\\15007\\Documents\\Kinect Studio\\BodyBasics-D2D\\save.bin'
save_path = 'C:\\Users\\15007\\Desktop\\生物竞赛\\angle.txt'
# 创建窗口
window = tk.Tk()

# 创建标签用于显示图像
image_label = tk.Label(window)
image_label.pack()

# 创建标签用于显示文字
custom_font = tkfont.Font(size=20)
text_label = tk.Label(window, font=custom_font)
text_label.pack()

# 打开摄像头
cap = cv2.VideoCapture(0)


def Get_angle(A, B, C):
    if isinstance(A, np.ndarray) and A.ndim == 2:
        BA = B - A
        BC = B - C
        AB_m = np.sqrt(BA[:, 0] ** 2 + BA[:, 1] ** 2 + BA[:, 2] ** 2)
        BC_m = np.sqrt(BC[:, 0] ** 2 + BC[:, 1] ** 2 + BC[:, 2] ** 2)
        angel = np.arccos(np.sum(BA * BC, axis=1) / (AB_m * BC_m))
    else:
        BA = B - A
        BC = B - C
        AB_m = np.sqrt(BA[0] ** 2 + BA[1] ** 2 + BA[2] ** 2)
        BC_m = np.sqrt(BC[0] ** 2 + BC[1] ** 2 + BC[2] ** 2)
        angel = np.arccos(np.sum(BA * BC) / (AB_m * BC_m))
    return angel


def update_frame():
    with open(path, 'rb') as file:
        binary_data = file.read()

    if binary_data:
        binary_data = np.array(binary_data)
        binary_data = str(binary_data)
        binary_data = binary_data.strip('b').strip("'").split(' ')
        binary_data = np.array([float(i) for i in binary_data])
        A = binary_data[:3]
        B = binary_data[3:6]
        C = binary_data[6:]
        angle = Get_angle(A, B, C)
        angle_degrees = np.degrees(angle)
        with open(save_path,'w') as file_save:
            file_save.write(str(180-angle_degrees))
        print(angle_degrees)

        # 显示角度
        text_label.config(text="Angle: {:.2f}".format(angle_degrees))

    ret, frame = cap.read()
    if ret:
        # 将OpenCV图像转换为PIL图像
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # 将PIL图像转换为Tkinter图像
        image_tk = ImageTk.PhotoImage(image)

        # 在标签上显示图像
        image_label.config(image=image_tk)
        image_label.image = image_tk

    # 更新帧
    window.after(1000 // 120, update_frame)


# 启动更新帧的函数
update_frame()

# 运行窗口主循环
window.mainloop()

# 释放摄像头资源
cap.release()
