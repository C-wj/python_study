import pandas as pd
import hashlib
from multiprocessing import Pool, cpu_count
import logging
import time
import os

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_and_encrypt_phone_numbers(args):
    phone, isp, temp_dir = args
    data = []
    for i in range(1, 10000):
        suffix = f"{i:04d}"  # 生成四位数的后缀，例如0001, 0002, ..., 9999
        combined_phone = f"{phone}{suffix}"
        md5_hash = hashlib.md5(combined_phone.encode()).hexdigest()
        data.append([phone, isp, combined_phone, md5_hash])
    temp_file = os.path.join(temp_dir, f"{phone}_{isp}.csv")
    pd.DataFrame(data, columns=['phone', 'isp', 'combined_phone', 'md5']).to_csv(temp_file, index=False)
    return temp_file

def process_chunk(chunk, province, isp, temp_dir):
    if isp:
        filtered_chunk = chunk[(chunk['province'] == province) & (chunk['isp'] == isp)]
    else:
        if province:
            filtered_chunk = chunk[chunk['province'] == province]
        else:
            filtered_chunk = chunk

    if filtered_chunk.empty:
        logging.info("No data found for the given province and ISP in this chunk.")
        return []  # 返回空列表

    args_list = [(row['phone'], row['isp'], temp_dir) for _, row in filtered_chunk.iterrows()]
    num_workers = min(cpu_count(), len(args_list))

    logging.info(f"Processing {len(args_list)} records with {num_workers} workers.")

    with Pool(num_workers) as pool:
        temp_files = pool.map(generate_and_encrypt_phone_numbers, args_list)

    return temp_files

def filter_and_encrypt_large_csv(file_path, province, isp, output_file, chunk_size=10000, encoding='utf-8'):
    reader = pd.read_csv(file_path, chunksize=chunk_size, encoding=encoding)
    temp_dir = "temp_data"
    os.makedirs(temp_dir, exist_ok=True)
    temp_files = []

    start_time = time.time()

    for i, chunk in enumerate(reader, 1):
        logging.info(f"Processing chunk {i}...")
        chunk_start_time = time.time()
        processed_files = process_chunk(chunk, province, isp, temp_dir)
        if processed_files:
            temp_files.extend(processed_files)
        logging.info(f"Chunk {i} processed in {time.time() - chunk_start_time:.2f} seconds.")

    if not temp_files:
        logging.info("No data found for the given province and ISP across all chunks.")
        return

    result_df = pd.concat([pd.read_csv(f) for f in temp_files])
    result_df.to_csv(output_file, index=False)

    # 删除临时文件
    for temp_file in temp_files:
        os.remove(temp_file)

    logging.info(f"All chunks processed in {time.time() - start_time:.2f} seconds.")
    logging.info(f"Filtered data saved to {output_file}")



if __name__ == '__main__':
    # 示例使用
    file_path = 'phone-qqzeng-202311-505323.csv'  # 输入的Excel文件路径
    province = '湖北'  # 将此替换为你要筛选的省份名称，如果不筛选省份则设置为None
    isp = '中国联通'  # 将此替换为你要筛选的ISP名称，或者设置为None表示不筛选ISP
    output_file = province + "_" + isp + '.csv'  # 输出的csv文件路径

    # 调用函数进行筛选并保存结果
    print(f"正在筛选 {file_path} 中的数据...")
    filter_and_encrypt_large_csv(file_path, province, isp, output_file)

    print(f"筛选结果已保存到 {output_file}")
