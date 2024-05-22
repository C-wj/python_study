import pandas as pd
from sqlalchemy import create_engine

# 创建数据库引擎
engine = create_engine('mysql+pymysql://root:sy666.com@192.168.1.200:3308/ota')

# 从数据库中读取数据
query = "SELECT `名称`, `编码`, `父级编码`, `状态` FROM `address`"
df = pd.read_sql_query(query, engine)

# 处理数据
province_city_county = {}

# 获取省级编码
province_codes = df[df['父级编码'] == '0']['编码'].unique()
for province_code in province_codes:
    province_name = df[df['编码'] == province_code]['名称'].values[0]
    province_city_county[province_code] = {
        'province_name': province_name,
        'cities': {}
    }

# 确定市级单位：父级是省级单位且该编码是其他编码的父级编码
city_codes = df[df['父级编码'].isin(province_codes) & df['编码'].isin(df['父级编码'].unique())]['编码'].unique()

# 先添加所有的市级单位
for _, row in df[df['编码'].isin(city_codes)].iterrows():
    code, name, parent_code = row['编码'], row['名称'], row['父级编码']
    if parent_code in province_codes:  # 确认父级是省级单位
        province_city_county[parent_code]['cities'][code] = {
            'city_name': name,
            'counties': {}
        }

# 添加县级单位
for _, row in df.iterrows():
    code, name, parent_code = row['编码'], row['名称'], row['父级编码']
    # 确认不是省级或市级单位（即，是县级单位）
    if code not in city_codes and parent_code in city_codes:
        for province_info in province_city_county.values():
            if parent_code in province_info['cities']:
                province_info['cities'][parent_code]['counties'][code] = name
                break

# 构造最终的数据列表
data = []
for province_code, province_info in province_city_county.items():
    for city_code, city_info in province_info['cities'].items():
        for county_code, county_name in city_info['counties'].items():
            data.append([province_code, province_info['province_name'], city_code, city_info['city_name'], county_code,
                         county_name])

columns = ['province_code', 'province_name', 'city_code', 'city_name', 'county_code', 'county_name']
transformed_df = pd.DataFrame(data, columns=columns)
print(transformed_df)
# 数据导入到新表
transformed_df.to_sql('cmcc_mobile_address_copy2', con=engine, if_exists='replace', index=False)
print("数据导入完成。")
