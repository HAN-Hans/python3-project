# python 基本数据结构

## str

```python
[
 '__add__',
 '__class__',
 '__contains__',
 '__delattr__',
 '__dir__',
 '__doc__',
 '__eq__',
 '__format__',
 '__ge__',
 '__getattribute__',
 '__getitem__',
 '__getnewargs__',
 '__gt__',
 '__hash__',
 '__init__',
 '__init_subclass__',
 '__iter__',
 '__le__',
 '__len__',
 '__lt__',
 '__mod__',
 '__mul__',
 '__ne__',
 '__new__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__rmod__',
 '__rmul__',
 '__setattr__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 'capitalize',  # 首字母大写其他小些
 'casefold',  # 转换为大小写不敏感的语句
 'center',  # 中间对齐
 'count',  # 计算子串个数
 'encode',
 'endswith',
 'expandtabs',
 'find',
 'format',
 'format_map',
 'index',
 'isalnum',  # 判断是否是数字或者字母
 'isalpha',
 'isdecimal',  # 判断只有十进制数字
 'isdigit',
 'isidentifier',  # 判断是否是Python保留字
 'islower',
 'isnumeric',
 'isprintable',
 'isspace',
 'istitle',  # 判断是否是标题
 'isupper',
 'join',
 'ljust',  # 左对齐并填相应字符
 'lower',
 'lstrip',
 'maketrans',  # 创建字符映射转换表,配合translate使用
 'partition',  # 创建标识符分割字符串
 'replace',
 'rfind',
 'rindex',
 'rjust',
 'rpartition',
 'rsplit',
 'rstrip',
 'split',
 'splitlines',
 'startswith',
 'strip',
 'swapcase',  # 转换大小写
 'title',
 'translate',  # 根据映射转换字符
 'upper',
 'zfill'  # 在字符串前面填充'0'
]
```


## list

```python
['__add__',
 '__class__',
 '__contains__',
 '__delattr__',
 '__delitem__',
 '__dir__',
 '__doc__',
 '__eq__',
 '__format__',
 '__ge__',
 '__getattribute__',
 '__getitem__',
 '__gt__',
 '__hash__',
 '__iadd__',
 '__imul__',
 '__init__',
 '__init_subclass__',
 '__iter__',
 '__le__',
 '__len__',
 '__lt__',
 '__mul__',
 '__ne__',
 '__new__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__reversed__',
 '__rmul__',
 '__setattr__',
 '__setitem__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 'append',
 'clear',
 'copy',
 'count',
 'extend',
 'index',
 'insert',
 'pop',  # pop可以制定某个元素
 'remove',
 'reverse',
 'sort'
 ]
```

## dict

```python
['__class__',
 '__contains__',
 '__delattr__',
 '__delitem__',
 '__dir__',
 '__doc__',
 '__eq__',
 '__format__',
 '__ge__',
 '__getattribute__',
 '__getitem__',
 '__gt__',
 '__hash__',
 '__init__',
 '__init_subclass__',
 '__iter__',
 '__le__',
 '__len__',
 '__lt__',
 '__ne__',
 '__new__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__setattr__',
 '__setitem__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 'clear',
 'copy',  # 浅拷贝
 'fromkeys',  # 从可迭代对象中设置为字典key,值为None
 'get',
 'items',
 'keys',
 'pop',
 'popitem',  # pop所有的key
 'setdefault',
 'update',
 'values'
]
```