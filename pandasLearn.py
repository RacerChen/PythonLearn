import pandas as pd

'''
参考资料：
Python pandas用法：https://www.jianshu.com/p/840ba135df30
pandas里面按条件筛选：https://www.jianshu.com/p/30254bc9fb40
'''
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002, 2003],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}

# 使用dict创建DataFrame
df = pd.DataFrame(data, columns=['year', 'state', 'pop'],
                  index=['one', 'two', 'three', 'four', 'five', 'six'])
# print(df)
'''
print(df)
       year   state  pop
one    2000    Ohio  1.5
two    2001    Ohio  1.7
three  2002    Ohio  3.6
four   2001  Nevada  2.4
five   2002  Nevada  2.9
six    2003  Nevada  3.2
'''
# print(df)
df_drop = df.drop(index=df.loc[((df['pop'] > 2) & (df['pop'] < 3))].index)
# print(df_drop)
'''
       year   state  pop
one    2000    Ohio  1.5
two    2001    Ohio  1.7
three  2002    Ohio  3.6
six    2003  Nevada  3.2
'''

# 筛选两列
df_sub = df[['year', 'state']]
# print(df_sub)
'''
       year   state
one    2000    Ohio
two    2001    Ohio
three  2002    Ohio
four   2001  Nevada
five   2002  Nevada
six    2003  Nevada
'''

# 加列
df_sub['new_col'] = {1, 2, 3, 4, 5, 6}
# print(df_sub)
'''
       year   state  new_col
one    2000    Ohio        1
two    2001    Ohio        2
three  2002    Ohio        3
four   2001  Nevada        4
five   2002  Nevada        5
six    2003  Nevada        6
'''


# 合并两个Dataframe
df_append = df_sub.append(df_sub, ignore_index=True)
print(df_append)

# 将df按照year这一列排序
df_sorted = df.sort_values(by='year', ascending=True)
# print(df_sorted)
'''
       year   state  pop
one    2000    Ohio  1.5
two    2001    Ohio  1.7
four   2001  Nevada  2.4
three  2002    Ohio  3.6
five   2002  Nevada  2.9
six    2003  Nevada  3.2
'''

df_sorted['col_sub'] = df_sorted['pop'] - df_sorted['year']
# print(df_sorted)
'''
       year   state  pop  col_sub
one    2000    Ohio  1.5  -1998.5
two    2001    Ohio  1.7  -1999.3
four   2001  Nevada  2.4  -1998.6
three  2002    Ohio  3.6  -1998.4
five   2002  Nevada  2.9  -1999.1
six    2003  Nevada  3.2  -1999.8
'''

# 隔行相减
df_sorted['shift_pop'] = df_sorted['pop'].shift(1)
# df_sorted['shift_pop'].iloc[0] = df_sorted['pop'].iloc[0]
# print(df_sorted)
# 构造一个下移的行
'''
       year   state  pop  shift_pop
one    2000    Ohio  1.5       NaN
two    2001    Ohio  1.7       1.5
four   2001  Nevada  2.4       1.7
three  2002    Ohio  3.6       2.4
five   2002  Nevada  2.9       3.6
six    2003  Nevada  3.2       2.9
'''
df_sorted['pop'] = df_sorted['pop'] - df_sorted['shift_pop']
del df_sorted['shift_pop']
# print(df_sorted)
# 相减，并删除temp行
'''
       year   state  pop
one    2000    Ohio  NaN
two    2001    Ohio  0.2
four   2001  Nevada  0.7
three  2002    Ohio  1.2
five   2002  Nevada -0.7
six    2003  Nevada  0.3
'''
# print(df_sorted)
'''
       year   state  pop
one    2000    Ohio  NaN
two    2001    Ohio  0.2
four   2001  Nevada  0.7
three  2002    Ohio  1.2
five   2002  Nevada -0.7
six    2003  Nevada  0.3
'''

# 改列名
df_sorted = df_sorted.rename(columns={'pop': 'pop_newname'})
# print(df_sorted)
'''
       year   state  pop_newname
one    2000    Ohio          NaN
two    2001    Ohio          0.2
four   2001  Nevada          0.7
three  2002    Ohio          1.2
five   2002  Nevada         -0.7
six    2003  Nevada          0.3
'''


# 重新刷一列
df_sorted['pop_newname'] = [1.0, 0.2, 1.2, 0.7, -0.7, 0.3]
'''
       year   state  pop_newname  col_sub
one    2000    Ohio          1.0  -1998.5
two    2001    Ohio          0.2  -1999.3
four   2001  Nevada          1.2  -1998.6
three  2002    Ohio          0.7  -1998.4
five   2002  Nevada         -0.7  -1999.1
six    2003  Nevada          0.3  -1999.8
'''
print(df_sorted)

df_sorted['pop_newname'].iloc[0] = 0
# print(df_sorted)

# 筛选index中的column的值，df.at[index, column]
df_filter = df.at['one', 'year']
# print(df_filter)
'''
2000
'''

# 筛选出条件的DataFrame
df_2001 = df.loc[df['year'] == 2001]
'''
print(df_2001)
      year   state  pop
two   2001    Ohio  1.7
four  2001  Nevada  2.4
'''

# 多条件筛选，一定要加括号
df_2001_nevada = df.loc[(df['year'] == 2001) & (df['state'] == 'Nevada')]
'''
print(df_2001_nevada)
      year   state  pop
four  2001  Nevada  2.4
'''

# 删除列
# del df['state', 'pop'] 不可以
del df['state']
del df['pop']
# print(df)
'''
       year
one    2000
two    2001
three  2002
four   2001
five   2002
six    2003
'''



