################################
### 1. 基本数据类型和运算符
################################

################################
# 整数与浮点数
3 + 2 # => 5
3.0 + 2.0  # => 5.0

## 除法会自动转换成浮点数
35 / 5  # => 7.0
5 / 3  # => 1.6666666666666667

## 整数除法的结果都是向下取整
5 // 3     # => 1
5.0 // 3.0 # => 1.0 # 浮点数也可以
-5 // 3  # => -2
-5.0 // 3.0 # => -2.0

## 模除
7 % 3 # => 1
7.0 % 2.5 # => 2

## x的y次方
2**4 # => 16


################################
# 布尔运算
## 布尔值首字母一定大写
True 
False

## 用not取非
not True  # => False
not False  # => True

## 逻辑运算符，注意and和or都是小写
True and False #=> False
False or True #=> True
0 and 2 #=> 0
-5 or 0 #=> -5

## 用==判断相等
0 == False #=> True
2 == True #=> False
1 == True #=> True

## 用!=判断不等
1 != 1  # => False
2 != 1  # => True

## 比较大小
1 < 10  # => True
1 > 10  # => False
2 <= 2  # => True
2 >= 2  # => True

## 大小比较可以连起来！
1 < 2 < 3  # => True
2 < 3 < 2  # => False

################################
# 字符串
## 字符串用单引双引都可以
"这是个字符串"
'这也是个字符串'

## 可以加法与乘法运算
"Hello " + "world!"  # => "Hello world!"
"Hello "*3 # => 'Hello Hello Hello '

## 字符串可以被当作字符列表
"This is a string"[0:6]  # => 'This i'

## 用.format来格式化字符串
"{} can be {}".format("strings", "interpolated")

## 可以重复参数以节省时间
"{0} be nimble, {0} be quick, {0} jump over the {1}".format("Jack", "candle stick") #=> "Jack be nimble, Jack be quick, Jack jump over the candle stick"

## 如果不想数参数，可以用关键字
"{name} wants to eat {food}".format(name="Bob", food="lasagna") #=> "Bob wants to eat lasagna"

# MSIC.
##  None是一个对象
type(None)  # => <class 'NoneType'>

## 当与None进行比较时不要用 ==，要用is。is是用来比较两个变量是否指向同一个对象。
"etc" is None  # => False
None is None  # => True

## None，0，空字符串，空列表，空字典布尔值都是False
# 所有其他值都是True
bool(0)  # => False
bool("")  # => False
bool([]) #=> False
bool({}) #=> False



################################
### 2. 变量和集合
################################

# 变量
## 传统的变量命名是小写，用下划线分隔单词
some_var = 5
some_var  # => 5

## 常见保留字

## global


# 列表
li = []
other_li = [4, 5, 6]
mix_li = [1,2,3,"hello",["python","C++"]]

## 加法和数乘
add_li = [1, 2, 3] + [4, 5, 6]; add_li # => [1, 2, 3, 4, 5, 6]
mul_li = [1]*5; mul_li # => [1, 1, 1, 1, 1]

## 用append在列表最后追加元素
li.append(1)    # li现在是[1]
li.append(2)    # li现在是[1, 2]
li.append(4)    # li现在是[1, 2, 4]
li.append(3)    # li现在是[1, 2, 4, 3]
## 用pop从列表尾部删除
li.pop()        # => 3 且li现在是[1, 2, 4]
## 把3再放回去
li.append(3)    # li变回[1, 2, 4, 3]
