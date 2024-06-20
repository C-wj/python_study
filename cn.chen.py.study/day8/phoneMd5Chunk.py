import hashlib
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count

import pandas as pd

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_and_encrypt_phone_numbers(args):
    phone, isp = args
    data = []
    for i in range(1, 10000):
        suffix = f"{i:04d}"  # 生成四位数的后缀，例如0001, 0002, ..., 9999
        combined_phone = f"{phone}{suffix}"
        md5_hash = hashlib.md5(combined_phone.encode()).hexdigest()
        data.append([phone, isp, combined_phone, md5_hash])
    return pd.DataFrame(data, columns=['phone', 'isp', 'combined_phone', 'md5'])


def process_chunk(chunk, province, isp):
    if isp:
        filtered_chunk = chunk[(chunk['province'] == province) & (chunk['isp'] == isp)]
    else:
        if province:
            filtered_chunk = chunk[chunk['province'] == province]
        else:
            filtered_chunk = chunk

    if filtered_chunk.empty:
        logging.info("No data found for the given province and ISP in this chunk.")
        return pd.DataFrame()  # 返回空的DataFrame

    args_list = [(row['phone'], row['isp']) for _, row in filtered_chunk.iterrows()]
    num_workers = min(cpu_count(), len(args_list))

    logging.info(f"Processing {len(args_list)} records with {num_workers} workers.")

    with Pool(num_workers) as pool:
        results = pool.map(generate_and_encrypt_phone_numbers, args_list)

    return pd.concat(results)


def write_to_excel(df, output_file, sheet_name):
    with pd.ExcelWriter(output_file, engine='openpyxl', mode='a' if os.path.exists(output_file) else 'w') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    logging.info(f"Written {len(df)} records to {sheet_name} in {output_file}.")


def filter_and_encrypt_large_csv(file_path, province, isp, output_file, chunk_size=10000, sheet_size=500000,
                                 encoding='utf-8'):
    reader = pd.read_csv(file_path, chunksize=chunk_size, encoding=encoding)
    chunks = []
    total_records = 0
    sheet_index = 1

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        for i, chunk in enumerate(reader, 1):
            logging.info(f"Processing chunk {i}...")
            chunk_start_time = time.time()
            processed_chunk = process_chunk(chunk, province, isp)
            if not processed_chunk.empty:
                chunks.append(processed_chunk)
                total_records += len(processed_chunk)

                if total_records >= sheet_size:
                    combined_df = pd.concat(chunks)
                    chunks = []  # 清空缓存的块
                    executor.submit(write_to_excel, combined_df, output_file, sheet_name=f'Sheet{sheet_index}')
                    sheet_index += 1
                    total_records = 0  # 重置计数器

            logging.info(f"Chunk {i} processed in {time.time() - chunk_start_time:.2f} seconds.")

        if chunks:
            combined_df = pd.concat(chunks)
            executor.submit(write_to_excel, combined_df, output_file, sheet_name=f'Sheet{sheet_index}')

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
