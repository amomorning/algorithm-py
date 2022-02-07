
## PyGraphViz
PyGraphviz 是对 Graphviz 的封装，提供了 Python 接口的调用。Graphviz 是一个开源软件包，提供了对图、点、边的简易操作，所以封装后的 PyGraphviz 可以很容易用来绘制想要的图形。

### 安装

#### Windows
1. 首先需要 GraphViz 软件，[安装 GraphViz](http://www.graphviz.org/download/)，在安装时需要勾选 `添加到PATH`
2. [下载合适版本 pygraphviz.whl](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygraphviz)，注意平台(`win_amd64`)和 python 版本(`cp38`)
3. 打开下载目录，命令行安装 pygraphviz:
	``` bash
	pip install .\pygraphviz-1.7-cp38-cp38-win_amd64.whl
	```
#### Linux
``` bash
sudo apt install graphviz
pip install pygraphviz
```

### 使用
导入：
``` python
import pygraphviz as pgv
```
建图：

``` python
A = pgv.AGraph()
```
加边：
``` python
A.add_edge(1, 2)
```

添加属性：
``` py
G.add_node(1, color="red")
G.add_edge("b", "c", color="blue")

n = G.get_node(1)
n.attr["shape"] = "box"

e = G.get_edge("b", "c")
e.attr["color"] = "green"
```

导出 dot 文件：
``` py
print( A.string() )
```
绘图：
- 格式可为： `canon`, `cmap`, `cmapx`, `cmapx_np`, `dia`, `dot`, `fig`, `gd`, `gd2`, `gif`, `hpgl`, `imap`, `imap_np`, `ismap`, `jpe`, `jpeg`, `jpg`, `mif`, `mp`, `pcl`, `pdf`, `pic`, `plain`, `plain-ext`, `png`, `ps`, `ps2`, `svg`, `svgz`, `vml`, `vmlz`, `vrml`, `vtx`, `wbmp`, `xdot`, `xlib`
- prog 包括：`neato`, `dot`, `twopi`, `circo`, `fdp`, `nop`
``` py
A.draw("filename.png", prog="neato")
```
从 Networkx 转换过来：
``` py
A = nx.nx_agraph.to_agraph(G)
```

## Networkx
### 安装
``` bash
pip install networkx
```

### 使用
#### 定义
#### 算法

### 链接
- [Reference](https://networkx.org/documentation/stable/reference/index.html)
- [Examples](https://networkx.org/documentation/stable/auto_examples/index.html)

## OSMnx
