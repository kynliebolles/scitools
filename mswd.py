import numpy as np

def calculate_mswd(values, errors_2se):
    results = []
    for i in range(len(values)):
        # 将 2SE 转换为 1SE (除以 2)
        errors_1se = errors_2se[i] / 2

        # 计算加权均值
        weighted_mean = np.sum(values[i] / errors_1se**2) / np.sum(1 / errors_1se**2)
        
        # 计算 MSWD
        N = len(values[i])  # 测量值数量
        if N > 1:
            mswd = np.sum(((values[i] - weighted_mean)**2) / errors_1se**2) / (N - 1)
        else:
            mswd = np.nan
        
        results.append({
            'group': f'VALUE{i+1}',
            'weighted_mean': weighted_mean,
            'mswd': mswd
        })
    return results