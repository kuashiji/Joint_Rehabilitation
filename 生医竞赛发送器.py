import socket
import time
import os

def read_last_line(file_path):
    try:
        with open(file_path, 'r') as file:
            # 读取第一个字符
            first_char = file.read(1)
            # 移动文件指针到文件末尾
            file.seek(0, 2)
            # 获取当前文件指针位置
            position = file.tell()
            # 向前读取，直到找到换行符
            while position > 0:
                position -= 1
                file.seek(position, 0)
                if file.read(1) == '\n':
                    break
            # 返回最后一行内容
            return first_char + file.readline().strip()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""


def send_data(data, host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(data.encode(), (host, port))
            print(f"Sent data to {host}:{port}: {data}")  # 添加这一行输出
    except Exception as e:
        print(f"Error sending data: {e}")

def main():
    unity_host = '10.163.14.141'  # Unity 的主机地址
    unity_port = 12345  # Unity 的端口号
    angle_file_path = 'C:\\Users\\15007\\Desktop\\生物竞赛\\angle.txt'  # 角度文件路径
    type_file_path = 'C:\\Users\\15007\\Desktop\\生物竞赛\\type.txt'  # 类型文件路径

    last_modified_time = 0

    while True:
        # 检查类型文件是否有更新
        current_modified_time = os.path.getmtime(type_file_path)
        if current_modified_time != last_modified_time:
            # 读取类型文件最后一行内容并发送给 Unity
            type_data = read_last_line(type_file_path)
            send_data(type_data, unity_host, unity_port)
            last_modified_time = current_modified_time

        # 读取角度文件最后一行内容并发送给 Unity
        angle_data = read_last_line(angle_file_path)
        print("Angle data read from file:", angle_data)

        send_data(angle_data, unity_host, unity_port)

        time.sleep(1//30)  # 延迟一段时间后再次发送

if __name__ == "__main__":
    main()
