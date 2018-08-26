class Hello(object):
    def hello(self, name='world'):
        print('Hello,%s.' % name)


type(Hello)  # <class 'type'>
type('Hello', (object,), dict(hello=map))  # 动态创建类


class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)


# 定义类的时候还要指示使用ListMetaclass来定制类，传入关键字参数metaclass
class MyList(list, metaclass=ListMetaclass):
    pass


def foo(x):
    print(f"{x}")


class A(object):
    # __slots__定义的属性仅对当前类起作用,对继承的子类是不起作用的
    # 除非在子类中也定义__slots__,这样,子类允许定义的属性就是自身的__slots__加上父类的__slots__
    __slots__ = ('name', 'var_of_instance', '_age')  # 限制实例属性
    var_of_class = 1  # 类属性

    def __init__(self, name):
        self.name = name
        self.var_of_instance = 0
        self._age = 0

    def foo(self, x):
        print(f"{self} -> {x}")

    @classmethod
    def class_foo(cls, x):
        print(f"{cls} ->{x}")

    @staticmethod
    def static_foo(x):
        print(f"{x}")

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age


foo(10)
a = A("han")
print(f"{a} -> {a.var_of_class} -> {a.var_of_instance}")
print(f"{a.__class__} -> {A.var_of_class} -> {a.__class__.var_of_class}")

# 实例方法需要绑定对应的实例,可通过实例调用,或者函数中传入实例
a.foo(123)  # 123
# A.foo(123)  # TypeError: foo() missing 1 required positional argument: 'x'
A.foo(a, 456)  # 456
A.foo(A, 789)  # 789
# 类方法是绑定到类的
A.class_foo(123)  # 123
a.class_foo(456)  # 456
# 静态方法就和普通方法一样,只不过是放在类中,方便使用
A.static_foo(456)  # 123
a.static_foo(456)  # 456

# 可以给类动态添加属性,但是无法对实例添加slots之外属性,会报错
A.pk = 10
print(A.pk)  # 10
# a.bk = 10  # AttributeError: 'A' object has no attribute 'bk'

# 通过@property可以为实例添加属性
print(a.age)
a.age = 10
print(a.age)


# python中抽象函数
from abc import ABC, abstractmethod


class A(ABC):
    @abstractmethod
    def abstract_method(self):
        """ 在子类中实现该方法,才可以实例话 """


class SubA(A):
    def abstract_method(self):
        print("必须实现abstract method才可以实例话")


# a = A()  # TypeError: Can't instantiate abstract class A with abstract methods abstract_method
b = SubA()

# Iterable 可迭代对象,可以使用for...in...都是可迭代对象
li = [x*x for x in range(10)]  # 列表生成器一次性将所有元素读入到内存中
# Generators 迭代器,每次只能迭代一次,不会将所有值存储在内存中，它们会动态生成值
ge = (x*x for x in range(10))  # 由于生成器只能使用一次,读完就会删掉
def gn():
    for i in range(3):
        n = yield i*i  # 使用yield生成器
        print(n)
g = gn()  # 调用的时候不会执行函数体,而是返回生成器对象
for i in g:  # 用for可以执行函数,但是每次执行回到yield返回
    print(i)
print("============")
g = gn()
print(next(g))  # 生成器可以使用next()函数执行
print(g.__next__())
print(next(g))
# print(next(g))  # StopIteration 最后一个迭代完在使用会报错
print("============")
g = gn()
print(g.send(None))  # 生成器也可以使用send()迭代,第一次参数必须是None
print(g.send(1))  # next(g)相当于g.send(None)
print(g.send(2))
# print(g.send(3))  # StopIteration 最后一个迭代完在使用会报错


import sys
l = []
a = l
r = []
b = r
r.append(l)
l.append(r)
print(sys.getrefcount(a))  # 3
print(sys.getrefcount(b))  # 3
del l
del r
print(sys.getrefcount(a))  # 3
print(sys.getrefcount(b))  # 3

