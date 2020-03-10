""" 常用元字符
. 匹配任意字符
^ 匹配字符串开始位置
$ 匹配字符串中结束的位置
* 前面的原子重复0次、1次、多次
? 前面的原子重复0次或者1次
+ 前面的原子重复1次或多次
{n} 前面的原子出现了 n 次
{n,} 前面的原子至少出现 n 次
{n,m} 前面的原子出现次数介于 n-m 之间
( ) 分组,需要输出的部分
"""

""" 常用通用字符
\s  匹配空白字符
\w  匹配任意字母/数字/下划线
\W  和小写 w 相反，匹配任意字母/数字/下划线以外的字符
\d  匹配十进制数字
\D  匹配除了十进制数以外的值
[0-9]  匹配一个0-9之间的数字
[a-z]  匹配小写英文字母
[A-Z]  匹配大写英文字母
""" 

import re


# 查找第一个匹配
s = 'i love python very much'
pat = 'python'
r = re.search(pat,s)
print(r.span()) #(7,13)


# 查找浮点数和整数
s = '1共20行代码运行时间13.59s'
pat = r'\d+\.\d+|\d+' # A|B，匹配A失败才匹配B
re.findall(pat,s)
# ['1', '20', '13.59']


# re.I忽略大小写
s = 'That'
pat = r't'
re.findall(pat,s,re.I)


# 多次匹配用compile
pat = re.compile('\W+')
pat.findall('ed#2@edc')
pat.findall('guozhennianhua@163.com')


# 分割字符串
s = 'This module provides regular expression matching operations similar to those found in Perl'
pat = r'\s+'
r = re.split(pat,s)
# ['This', 'module', 'provides', 'regular', 'expression', 'matching', 'operations', 'similar', 'to', 'those', 'found', 'in', 'Perl']


# 替换字符串
content="hello 12345, hello 456321"
pat=re.compile(r'\d+') #要替换的部分
m=pat.sub("666",content)
print(m) # hello 666, hello 666
