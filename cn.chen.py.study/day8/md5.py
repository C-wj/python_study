import hashlib
import os
import sys

import pandas as pd


# 读取Excel文件中的手机号码号段
def read_phone_segments(file_name):
    df = pd.read_excel(file_name, usecols=[0], dtype=str)
    phone_segments = df[df.columns[0]].tolist()
    return phone_segments


# 为每个号段生成0001到9999的号码，并写入TXT文件
def generate_and_write_numbers(segments, output_file):
    with open(output_file, 'w') as file:
        for segment in segments:
            for i in range(1, 10000):
                full_number = f"{segment}{i:04d}"
                md5_number = encode_md5(full_number)
                file.write(f"{md5_number}\n")


def encode_md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()


def split_file(input_file, filename, max_size=1e9):
    file_number = 1
    output_file = f'{filename}_part{file_number}.txt'
    output = open(output_file, 'w')
    current_size = 0

    with open(input_file, 'r') as f:
        for line in f:
            output.write(line)
            current_size += len(line.encode('utf-8'))

            if current_size >= max_size:
                output.close()
                file_number += 1
                output_file = f'{filename}_part{file_number}.txt'
                output = open(output_file, 'w')
                current_size = 0

    output.close()
    print(f"File has been split into {file_number} parts.")


# 主程序
if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    file_name, excel_suffix = os.path.splitext(os.path.basename(input_file))

    output_file = file_name + '填充后.txt'  # 输出TXT文件名，根据实际情况修改

    print('开始读取, 文件路径:' + input_file)

    segments = read_phone_segments(input_file)

    print('开始填充号码, 文件路径:' + input_file)
    generate_and_write_numbers(segments, output_file)

    print('开始切割文件, 文件路径:' + output_file)
    split_file(output_file, file_name)

    print('END-END-END-END-END-END-END-END-END-END-END')
