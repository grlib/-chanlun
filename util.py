import pandas as pd
import numpy as np

def remove_inclusion(df):
    """
    去除DataFrame中的K线包含关系。
    
    参数:
    df -- 包含K线数据的Pandas DataFrame，至少包含'high', 'low'两列。
    
    返回:
    一个新的DataFrame，其中已经去除了包含关系。
    """
    # 记录初始长度，用于检测是否还有包含关系需要处理
    temp_len = len(df)
    
    # 外层循环，持续处理直到没有更多的包含关系
    i = 0
    while i <= len(df) - 3:  # 确保至少有3行数据进行比较
        # 判断第i+2根K线是否与第i+1根K线存在包含关系
        if (df.iloc[i+2]['high'] >= df.iloc[i+1]['high'] and df.iloc[i+2]['low'] <= df.iloc[i+1]['low']) or \
           (df.iloc[i+2]['high'] <= df.iloc[i+1]['high'] and df.iloc[i+2]['low'] >= df.iloc[i+1]['low']):
            # 判断当前趋势是上升还是下降
            if df.iloc[i+1]['high'] > df.iloc[i]['high']:
                # 上升趋势，取高点的最大值和低点的最大值
                df.iloc[i+2, df.columns.get_loc('high')] = max(df.iloc[i+1:i+3]['high'])
                df.iloc[i+2, df.columns.get_loc('low')] = max(df.iloc[i+1:i+3]['low'])
            else:
                # 下降趋势，取高点的最小值和低点的最小值
                df.iloc[i+2, df.columns.get_loc('high')] = min(df.iloc[i+1:i+3]['high'])
                df.iloc[i+2, df.columns.get_loc('low')] = min(df.iloc[i+1:i+3]['low'])
            
            # 删除第i+1根K线
            df.drop(df.index[i+1], inplace=True)
            
            # 由于删除了一行，重置i为当前行，重新检查新合并的K线与下一根K线
            i = i
        else:
            # 如果没有包含关系，移动到下一根K线
            i += 1
    
    # 如果DataFrame的长度没有变化，说明没有更多的包含关系
    return df if len(df) == temp_len else remove_inclusion(df)

# 使用示例
# 假设df是包含K线数据的DataFrame
# new_df = remove_inclusion(df)