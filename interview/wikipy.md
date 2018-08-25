1. **Python中万物皆对象,对象有可变(mutable)与不可变(immutable)对象**

在python中,strings,tuples,和numbers是不可变的对象,而 list,dict,set 等则是可变的对象可变对象在修改的时候只修改对象本身,不可变对象在修改时候会重新新建一个新的对象,将修改后的值传递给它

当一个引用传递给函数的时候,函数自动复制一份引用,这个函数里的引用和外边的引用没有半毛关系了而在参数传递的时候变量都是通过传递对象的引用（指针）,如果在域内修改不可变对象,将会创建新的对象,Python中没有块变量域

2. **元类(metaclass)**

`type()`函数既可以返回一个对象的类型,又可以创建出新的类型
``` python
class Hello(object):
    def hello(self,name='world'):
        print('Hello,%s.' % name)
type(Hello)  # <class 'type'>

type('Hello',(object,),dict(hello=fn))  # 动态创建类
```
除了使用`type()`动态创建类以外,要控制类的创建行为,还可以使用`metaclass`,metaclass的类名总是以`Metaclass`结尾,以便清楚地表示这是一个metaclass:
``` python
# metaclass是类的模板，所以必须从`type`类型派生：
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)
# 定义类的时候还要指示使用ListMetaclass来定制类，传入关键字参数metaclass
class MyList(list, metaclass=ListMetaclass):
    pass
```

3. **@staticmethod,@classmethod,@property,@abstractmethod**

``` python
def foo(x):
    print(f"{x}")


class A(object):
    # __slots__定义的属性仅对当前类起作用,对继承的子类是不起作用的
    # 除非在子类中也定义__slots__,这样,子类允许定义的属性就是自身的__slots__加上父类的__slots__
    __slots__ = ('name', 'var_of_instance')  # 限制实例属性
    var_of_class = 1  # 类属性

    def __init__(self, name):
        self.name = name
        self.var_of_instance = 0

    def foo(self, x):
        print(f"{self} -> {x}")

    @classmethod
    def class_foo(cls, x):
        print(f"{cls} ->{x}")

    @staticmethod
    def static_foo(x):
        print(f"{x}")


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
```

