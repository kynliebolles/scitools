import numpy as np

def calculate_ucrm(data):
    # 计算 u_char
    u_char = np.mean([np.mean(data[f'2SE{i}']) / 2 for i in range(1, 5)])

    # 计算 u_bb
    mean_values = [np.mean(data[f'VALUE{i}']) for i in range(1, 5)]
    u_bb = np.std(mean_values)

    # 计算 u_lts
    all_values = np.concatenate([data[f'VALUE{i}'] for i in range(1, 5)])
    u_lts = np.std(all_values)

    # 计算 UCRM
    k = 2  # 覆盖因子
    u_crm = k * np.sqrt(u_char**2 + u_bb**2 + u_lts**2)
    # 计算所有VALUE的平均值
    overall_mean = np.mean(all_values)

    return {
        "u_char": u_char,
        "u_bb": u_bb,
        "u_lts": u_lts,
        "UCRM": u_crm,
        "overall_mean": overall_mean
    }