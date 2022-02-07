# 在 PyPy 中字符串的 += 复杂度是 o(|s|)，而 CPython 中为 o(1)，在这种情况下会出现 PyPy TLE 而 CPython AC 的情况
# 参考 https://codeforces.com/blog/entry/86987
# 文档 https://doc.pypy.org/en/latest/cpython_differences.html
mylist = '123214'

s = ''
for ch in mylist:
    s += ch


# 正确的写法应该是：
parts = []
for ch in mylist:
    parts.append(ch)
s = "".join(parts)
