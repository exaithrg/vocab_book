import os
import json
from collections import defaultdict
from datetime import datetime

# 获取当前日期并格式化为字符串
current_date = datetime.now().strftime('%Y%m%d')

# 定义需要合并的JSON文件路径
json_files = [
    'counter-202411.json',
    'counter-202412_ISCL404.json',
    'counter-202412.json'
]

# 创建一个默认为整数0的字典来存储合并后的数据
merged_data = defaultdict(int)

# 遍历所有JSON文件并合并数据
for file in json_files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for key, value in data.items():
            merged_data[key] += value

# 将合并后的结果保存到一个新的JSON文件中，文件名包含当前日期，并且按键排序
output_file = f'merged_counter-{current_date}.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(dict(merged_data), f, ensure_ascii=False, indent=4, sort_keys=True)

print(f"所有JSON文件已成功合并并排序后保存到 '{output_file}' 中")
