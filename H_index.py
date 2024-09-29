import numpy as np

def calculate_h_index(data):
    # 提取数据
    values = [data[f'VALUE{i}'] for i in range(1, 5)]
    se_values = [data[f'2SE{i}'] for i in range(1, 5)]

    # 将所有值和SE值合并
    all_values = np.concatenate(values)
    all_se = np.concatenate(se_values)

    # 将2SE转换为1SE
    all_se = all_se / 2

    # 计算所有值的平均值
    mean_value = np.mean(all_values)

    # 计算每个值的H指数
    h_index = np.abs(all_values - mean_value) / all_se

    # 计算总体平均H指数
    mean_h_index = np.mean(h_index)

    return h_index, mean_h_index