import pandas as pd
import hashlib  # 确保导入了hashlib模块


def filter_by_province_and_optional_isp(file_path, province, isp, output_file):
    """
    根据给定的省份和可选的ISP筛选Excel文件中的数据，并将结果保存到新的Excel文件中。

    :param file_path: 输入的Excel文件路径
    :param province: 要筛选的省份
    :param isp: 要筛选的ISP（如果为空，则不作为筛选条件）
    :param output_file: 输出的Excel文件路径
    """
    # 读取Excel文件
    df = pd.read_excel(file_path)

    if isp:
        # 筛选出province列中等于给定值且isp列中等于给定值的数据
        filtered_df = df[(df['province'] == province) & (df['isp'] == isp)]
    else:
        if province:
            # 仅筛选出province列中等于给定值的数据
            filtered_df = df[df['province'] == province]
        else:
            filtered_df = df

    # 将筛选结果保存到新的Excel文件中
    filtered_df.to_excel(output_file, index=False)

    # 读取保存的文件
    df_filtered = pd.read_excel(output_file)

    # 对phone列进行MD5加密
    df_filtered['md5'] = df_filtered['phone'].apply(lambda x: hashlib.md5(str(x).encode()).hexdigest())

    # 将结果保存到新的Excel文件中
    df_filtered.to_excel(output_file, index=False)


if __name__ == '__main__':
    # 示例使用
    file_path = 'phone-qqzeng-202311-505323.xlsx'
    province = ''  # 将此替换为你要筛选的省份名称
    isp = ''  # 将此替换为你要筛选的ISP
    output_file = province + "_" + isp + '.xlsx'  # 输出的Excel文件路径

    # 调用函数进行筛选并保存结果
    print(f"正在筛选 {file_path} 中的数据...")
    filter_by_province_and_optional_isp(file_path, province, isp, output_file)

    print(f"筛选结果已保存到 {output_file}")
