import pandas as pd

a=pd.DataFrame({'a':[1,2,3],'b':[2,3,4]})
print(a)
'''
   a  b
0  1  2
1  2  3
2  3  4
'''
b=pd.DataFrame({'a':[2,22,3],'c':[22,33,44]})
print(b)
'''
    a   c
0   2  22
1  22  33
2   3  44
'''

# pandas合并，类似于数据库主键合并
c=pd.merge(a,b)
print(c)
'''
   a  b   c
0  2  3  22
1  3  4  44
'''


a = {}
a['1'] = 'test'
print(a)