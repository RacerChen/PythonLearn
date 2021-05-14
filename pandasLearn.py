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

