import json

import pandas as pd

# 读取Excel文件
excel_file_path = 'D:\\study\\迭代\\号卡\\移动\\深圳API对接技术文档_20230927(1)\\深圳API对接技术文档_20230927\\6. 省市区编码字典.xlsx'
df = pd.read_excel(excel_file_path)

# 初始化存储结构
province_city_county = {}

# 确定省级单位：存在下级编码且父编码为0（这里假设国家级编码为0，您需要根据实际情况调整）
province_codes = df[df['父级编码'] == 0]['编码'].unique()
for province_code in province_codes:
    province_name = df[df['编码'] == province_code]['名称'].values[0]
    province_city_county[str(province_code)] = {
        'province_name': province_name,
        'cities': {}
    }

# 确定市级单位和县级单位
for _, row in df.iterrows():
    code, name, parent_code = row['编码'], row['名称'], row['父级编码']
    if parent_code in province_codes:  # 市级单位
        # 检查市级单位是否有下级单位，如果没有，则将其视为县级单位
        if df[df['父级编码'] == code].empty:
            for province_code, province_info in province_city_county.items():
                if parent_code in province_info['cities']:
                    province_city_county[province_code]['cities'][str(parent_code)]['counties'][str(code)] = name
                    break
        else:
            province_city_county[str(parent_code)]['cities'][str(code)] = {
                'city_name': name,
                'counties': {}
            }
    elif parent_code in df[df['父级编码'].isin(province_codes)]['编码'].values:  # 县级单位
        for province_code, province_info in province_city_county.items():
            if parent_code in province_info['cities']:
                province_city_county[province_code]['cities'][str(parent_code)]['counties'][str(code)] = name
                break

# 将字典转换为JSON字符串
json_data = json.dumps(province_city_county, ensure_ascii=False, indent=4)

# 如果您想将JSON字符串保存到文件中，可以使用以下代码
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(province_city_county, json_file, ensure_ascii=False, indent=4)

# city_count = 0
# # 遍历所有province_codes 打印所有市
# for province_code in province_codes:
#     # 打印带有层级
#     print("省", province_code, "有城市数量", len(province_city_county[province_code]['cities']))
#     for parent_code, parent_info in province_city_county.items():
#         if parent_code == province_code:
#             city_count += len(parent_info['cities'])
#             for city_code, city_info in parent_info['cities'].items():
#                 print(city_code, city_info['city_name'])
#                 for county_code, county_name in city_info['counties'].items():
#                     # 打印带有层级
#                     print("    ", county_code, county_name)
#
# 转换为列表格式以便创建DataFrame
for province_code, province_info in province_city_county.items():
    for city_code, city_info in province_info['cities'].items():
        for county_code, county_name in city_info['counties'].items():
            data.append([province_code, province_info['province_name'], city_code, city_info['city_name'], county_code,
                         county_name])

# 将列表转换为DataFrame
columns = ['province_code', 'province_name', 'city_code', 'city_name', 'county_code', 'county_name']
transformed_df = pd.DataFrame(data, columns=columns)

# print(transformed_df)
# transformed_df.to_sql('cmcc_mobile_address', con=engine, if_exists='replace', index=False)
print("数据导入完成。")
