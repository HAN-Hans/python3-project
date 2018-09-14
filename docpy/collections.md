# collections 包

最近在AC一些算法题, 老是出现时间复杂度过大问题, 算法上面实在想不出怎么优化, 就想着用python的collections模块处理, 这样难度和处理的效率比自己想的快的多

首先看下collections模块源码的注释:

''' This module implements specialized container datatypes providing
alternatives to Python's general purpose built-in containers, dict,
list, set, and tuple.

* namedtuple   factory function for creating tuple subclasses with named fields
* deque        list-like container with fast appends and pops on either end
* ChainMap     dict-like class for creating a single view of multiple mappings
* Counter      dict subclass for counting hashable objects
* OrderedDict  dict subclass that remembers the order entries were added
* defaultdict  dict subclass that calls a factory function to supply missing values
* UserDict     wrapper around dictionary objects for easier dict subclassing
* UserList     wrapper around list objects for easier list subclassing
* UserString   wrapper around string objects for easier string subclassing

'''

collections包中总共有9个类
__all__ = ['deque', 'defaultdict', 'namedtuple', 'UserDict', 'UserList',
            'UserString', 'Counter', 'OrderedDict', 'ChainMap']

## ChainMap

`ChainMap(*maps)`用来将多个dict(字典)组成一个list(只是比喻)，可以理解成合并多个字典，但和update不同，而且效率更高。

```python
from collections import ChainMap
a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}
m = ChainMap(a, b)  # ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m['a']  # 'A'
m['c']  # 'C'
a['c'] = 'E'
m  # ChainMap({'a': 'A', 'c': 'E'}, {'b': 'B', 'c': 'D'})
# maps属性用户可更新的映射列表
m.maps  # [{'a': 'A', 'c': 'E'}, {'b': 'B', 'c': 'D'}]
# new_child(m=None)创建一个想的子上下文
m2 = m.new_child()  # ChainMap({}, {'a': 'A', 'c': 'G'}, {'b': 'B', 'c': 'D'})
m2['c'] = 'F'  # ChainMap({'c': 'F'}, {'a': 'A', 'c': 'G'}, {'b': 'B', 'c': 'D'})
m2.maps  # [{'c': 'F'}, {'a': 'A', 'c': 'G'}, {'b': 'B', 'c': 'D'}]
# parents获取除第一个值之后的映射
m2.parents  # ChainMap({'a': 'A', 'c': 'E'}, {'b': 'B', 'c': 'D'})
```

## Counter

`Counter([iterable-or-mapping])`也是dict的一个subclass，它是一个无序容器，可以看做一个计数器，用来统计相关元素出现的个数。

```python
from collections import Counter
# Counter自动忽略计数小于一的元素
cnt = Counter()
for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
    cnt[word] += 1
cnt  ## Counter({'blue': 3, 'red': 2, 'green': 1}) 
cnt = Counter()
for ch in 'hello':
    cnt[ch] = cnt[ch] + 1
cnt  # Counter({'l': 2, 'o': 1, 'h': 1, 'e': 1})
c = Counter(a=4, b=2, c=0, d=-2)
# elementes()返回可迭代对象
sorted(c.elements())  # ['a', 'a', 'a', 'a', 'b', 'b'] 
# most_common(n=None)返回计数最大的n个数
Counter('abracadabra').most_common(3)  # [('a', 5), ('r', 2), ('b', 2)]
# subtract(iterable)
c = Counter(a=4, b=2, c=0, d=-2)
d = Counter(a=1, b=2, c=3, d=4)

c + d  # c[x] + d[x]  Counter({'a': 5, 'b': 4, 'c': 3, 'd': 2})
c - d  # c.subtract(d)  Counter({'a': 3})
c & d  # min(c[x], d[x])  Counter({'a': 1, 'b': 2})
c | d  # max(c[x], d[x])  Counter({'a': 4, 'b': 2, 'c': 3, 'd': 4})
+c  # Counter(a=4, b=2)
-c  # Counter(d=2)
c.subtract(d)  # Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})
```

## deque

list存储数据的优势在于按找索引查找元素会很快，但是插入和删除元素就很慢了，因为它是是单链表的数据结构。`deque([iterable[, maxlen]])`是为了高效实现插入和删除操作的双向列表，适合用于队列和栈，而且线程安全。

list只提供了append和pop方法来从list的尾部插入/删除元素，但是deque新增了appendleft/popleft允许我们高效的在元素的开头来插入/删除元素。而且使用deque在队列两端添加（append）或弹出（pop）元素的算法复杂度大约是O(1)，但是对于list对象改变列表长度和数据位置的操作例如 pop(0)和insert(0, v)操作的复杂度高达O(n)。由于对deque的操作和list基本一致，这里就不重复了。

如果未指定maxlen或为None，则deques可能会增长到任意长度。 否则，双端队列限制为指定的最大长度。 一旦有界长度双端队列已满，当添加新项目时，从对方端丢弃相应数量的项目。 有界长度deques提供类似于Unix中的尾部过滤器的功能。 它们还可用于跟踪仅涉及最近活动的事务和其他数据池。

```python
from collections import deque
d = deque('ghi')                 # make a new deque with three items
d.append('j')                    # add a new entry to the right side
d.appendleft('f')                # add a new entry to the left side
d  # deque(['f', 'g', 'h', 'i', 'j'])
d.pop()  # 'j'
d.popleft()  # 'f'
d  # deque(['g', 'h', 'i'])
d.extend('jkl')                  # add multiple elements at once
d  # eque(['g', 'h', 'i', 'j', 'k', 'l'])
d.rotate(1)                      # right rotation
d  # deque(['l', 'g', 'h', 'i', 'j', 'k'])
d.rotate(-1)                     # left rotation
d  # deque(['g', 'h', 'i', 'j', 'k', 'l'])
deque(reversed(d))               # make a new deque in reverse order
deque(['l', 'k', 'j', 'i', 'h', 'g'])
d.extendleft('abc')              # extendleft() reverses the input order
d  # deque(['c', 'b', 'a'])
d.mexlen  
```

## defaultdict

`defaultdict(default_factory)`在普通的dict(字典)之上添加了default_factory，使得key(键)不存在时会自动生成相应类型的value(值)，default_factory参数可以指定成list, set, int等各种合法类型。通常比setdefault()快。

```python
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = defaultdict(list)  
for k, v in s:
    d[k].append(v)
d  # defaultdict(list, {'yellow': [1, 3], 'blue': [2, 4], 'red': [1]})
```

## namedtuple

使用namedtuple(typename, field_names)命名tuple中的元素来使程序更具可读性

```python
Point = namedtuple('Point', ['x', 'y'])
p = Point(11, y=22)
p.x + p.y  # 33
p  # Point(x=11, y=22)
```

## OrderedDict

我们知道默认的dict(字典)是无序的，但是在某些情形我们需要保持dict的有序性，这个时候可以使用`OrderedDict([items])`，它是dict的一个subclass(子类)，但是在dict的基础上保持了dict的有序型，下面我们来看一下使用方法。

```python
d = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}  # regular unsorted dictionary
OrderedDict(sorted(d.items(), key=lambda t: t[0]))  # dictionary sorted by key
OrderedDict(sorted(d.items(), key=lambda t: t[1]))  # dictionary sorted by value
OrderedDict(sorted(d.items(), key=lambda t: len(t[0])))  # dictionary sorted by length of the key string

d = OrderedDict.fromkeys('abcde')  # OrderedDict([('a', None), ('b', None), ('c', None), ('d', None), ('e', None)])
# move_to_end(key, last=True)移动key到OrderdDict的尾或者头元素去掉
d.move_to_end('b')  # OrderedDict([('a', None), ('c', None), ('d', None), ('e', None), ('b', None)])
d.move_to_end('b', last=False)  # OrderedDict([('b', None), ('a', None), ('c', None), ('d', None), ('e', None)])
# popitem(last=True)将OrderedDict的尾或者头元素去掉
d.popitem()  # ('e', None)
d.popitem(last=False)  # ('b', None)
```

## UserDict

`UserDict([initialdata])`它是封装了一个字典类dict，主要使用来拷贝一个字典的数据，而不是共享同一份数据。在类成员data里拷贝了一份字典数据，如果没有提供初始数据，就保存为空的方式。底层字典可以作为属性访问。

```python
from collections import UserDict
d = {'a': 2, 'b': 3}
ud = UserDict(d)
print(d, ud)  # {'a': 2, 'b': 3} {'a': 2, 'b': 3}
del d['a']
print(d, ud)  # {'b': 3} {'a': 2, 'b': 3}
ud.data  # {'a': 2, 'b': 3}
```

## UserList

`UserList([list])`它是封装了一个列表类list，在这个类里，主要管理成员变量data，在初始化时会把列表数据拷贝到data成员上，如果没有初始化数据，那么成员变量data初始化为空的列表。通过这种方式，可以向列表添加新行为。底层列表可以作为属性访问。

```python
from collections import UserList
l = [1, 5, 6, 8]
ul = UserList(l)
print(l, ul)  # [1, 5, 6, 8] [1, 5, 6, 8] 
del l[2]
print(l, ul)  # [1, 5, 8] [1, 5, 6, 8]
ul.data  # [1, 5, 6, 8]
```

# UserString

`UserString(seq)`它是封装了一个字符串类str，构造一个字符串或者一个UNICODE字符串对象。构造时可以从初始化参数里拷贝到成员变量data，sequence支持bytes，str，UserString等类型。底层字符串可以作为属性访问。

```python
from collections import UserString
s = 'this for test'
us = UserString(s)
print(us)  # this for test
print(us.data)  # this for test
```
